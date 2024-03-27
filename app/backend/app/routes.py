from flask import Blueprint, render_template, request, jsonify, make_response
from .models import RobotPositionDB
import pydobot
import serial.tools.list_ports


# Database code

db = RobotPositionDB('database/db.json')

# Robo code

class InteliArm(pydobot.Dobot):
    def __init__(self, port=None, verbose=False):
        super().__init__(port=port, verbose=verbose)
    
    def movej_to(self, x, y, z, r, wait=True):
        super()._set_ptp_cmd(x, y, z, r, mode=pydobot.enums.PTPMode.MOVJ_XYZ, wait=wait)

    def movel_to(self, x, y, z, r, wait=True):
        super()._set_ptp_cmd(x, y, z, r, mode=pydobot.enums.PTPMode.MOVL_XYZ, wait=wait)
        


def encontrar_porta_dobot(porta_desejada):
    portas = serial.tools.list_ports.comports()
    for porta in portas:
        if porta.device == porta_desejada:
            return porta.device
    return None


def criar_robot():
    porta_selecionada = encontrar_porta_dobot('/dev/cu.usbmodem14301')
    if porta_selecionada is not None:
        return InteliArm(port=porta_selecionada, verbose=False)
    else:
        return None

robot = criar_robot()

actuactor_is_on = False
    


def check_movement(desired, actual, tolerance=3):
    return all(abs(d - a) <= tolerance for d, a in zip(desired, actual))


# Flask code
main = Blueprint('main', __name__)

# Feito
@main.route('/', methods=['GET'])
def index():
    return render_template('telainicial.html')

# Feito
@main.route('/control', methods=['GET'])
def control():
    return render_template('control.html')

# Feito
@main.route('/log', methods=['GET'])
def log():
    all_registry = db.get_all_data()
    return render_template('log.html', logs=all_registry)
    
@main.route('/delete_log/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    try:
        db.remove(doc_ids == log_id)
        return jsonify({'success': True, 'message': 'Log deleted successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# Feito
@main.route('/is_connected', methods=['GET'])
def is_connected():
    global robot
    robot = criar_robot()
    
    if robot is not None:
        return "<div class='alert alert-success justify-content-center text-center'> Robô conectado com sucesso. </div>"
    else:
        return "<div class='alert alert-danger justify-content-center text-center'> Robô não encontrado. </div>"

# Feito
@main.route('/home', methods=['GET', 'POST'])
def home():
    global robot
    robot = criar_robot()
    if robot is not None:
        print(f'Dobot conectado com sucesso')
    else:
        print('Porta do Dobot não encontrada.')
    
    position_home = (240, 0, 150, 0)
    
    try:
        robot.movej_to(240,0,150,0, wait=True)
        
        current_position = robot.pose()
        
        if check_movement(position_home, current_position):
            work_status = "Sucesso"
        else:
            work_status = "Falha"
            
        db.insert_position(*position_home, work_status)
        
        return jsonify({'success': True, 'message': 'Position inserted successfully.', 'work': work_status})

    except Exception as e:
                return jsonify({'success': False, 'message': str(e)}), 500

# Feito     
       
@main.route('/actual_position', methods=['GET'])
def actual_position():
    global robot 
    robot = criar_robot()

    if robot is not None:
        print(f'Dobot conectado com sucesso')
    else:
        print('Porta do Dobot não encontrada.')
        
    position = robot.pose()
    
    position_data = {
        'x': position[0],
        'y': position[1],
        'z': position[2],
        'r': position[3]
    }
    return jsonify(position_data)


# Falta aplicar mudança estado atuador
@main.route('/actuactor', methods=['GET', 'POST'])
def actuator():
    global actuactor_is_on, robot
    robot = criar_robot()

    if robot is not None:
        if request.method == 'POST':
            # Alterna o estado do atuador
            actuactor_is_on = not actuactor_is_on
            robot.suck(actuactor_is_on)

        # Retorna o estado atual do atuador junto com a resposta
            if actuactor_is_on:
                html_response = "<div>O atuador está ligado.</div>"
            else:
                html_response = "<div>O atuador está desligado.</div>"
                
            return make_response(html_response)
    else:
        print('Porta do Dobot não encontrada.')
        return jsonify({'success': False, 'message': 'Porta do Dobot não encontrada.'}), 404



# Feito
@main.route('/move_robot', methods=['GET', 'POST'])
def move_robot():
    global robot
    robot = criar_robot()
    
    if robot is not None:
        print(f'Dobot conectado com sucesso')
        if request.method == 'POST':
            content = request.form # Usa get_json() para pegar o corpo JSON da requisição
            
            # Checa se todas as chaves necessárias estão no JSON
            if not all(key in content for key in ('x', 'y', 'z', 'r')):
                return jsonify({'success': False, 'message': 'Missing one or more required fields: x, y, z, r.'}), 400
            
            # Converte os valores para inteiros
            try:
                position = (int(content['x']), int(content['y']), int(content['z']), int(content['r']))
            except ValueError:
                # Retorna um erro se a conversão de algum dos valores falhar
                return jsonify({'success': False, 'message': 'All coordinates must be integer values.'}), 400

            try:
                print(*position)
                robot.movej_to(*position, wait=True)
                current_position = robot.pose()
                work_status = "Sucesso" if check_movement(position, current_position) else "Falha"
                
                db.insert_position(*position, work_status)
                return jsonify({'success': True, 'message': 'Position inserted successfully.', 'work': work_status})
            except Exception as e:  # Captura qualquer exceção para evitar falhas no servidor
                return jsonify({'success': False, 'message': str(e)}), 500
        else:
            
            return jsonify({'success': False, 'message': 'Method Not Allowed'}), 405
    else:
        print('Porta do Dobot não encontrada.')
        return jsonify({'success': False, 'message': 'Porta do Dobot não encontrada.'}), 404
        
    