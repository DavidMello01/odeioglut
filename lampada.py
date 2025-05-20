import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Controle de rotação do cubo com o mouse
rot_x, rot_y = 0, 0
last_x, last_y = 0, 0
mouse_pressed = False

# Variáveis para controle da luz
angulo_luz = 0

def mouse_button_callback(window, button, action, mods):
    global mouse_pressed
    if button == glfw.MOUSE_BUTTON_LEFT:
        mouse_pressed = action == glfw.PRESS

def cursor_position_callback(window, xpos, ypos):
    global last_x, last_y, rot_x, rot_y, mouse_pressed
    if mouse_pressed:
        dx = xpos - last_x
        dy = ypos - last_y
        rot_x += dy * 0.5
        rot_y += dx * 0.5
    last_x = xpos
    last_y = ypos

def init_window(width, height, title):
    if not glfw.init():
        raise Exception("GLFW não pôde ser inicializado")
    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception("Janela GLFW não pôde ser criada")
    glfw.make_context_current(window)

    # Registra callbacks do mouse
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)

    return window

def configurar_luz():
    # Configura a luz do "sol" (deixa a luz rotacionando)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    # A luz ficará em movimento contínuo (simula o sol)
    luz_pos = [2.0 * np.cos(np.radians(angulo_luz)), 2.0, 2.0 * np.sin(np.radians(angulo_luz)), 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, luz_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.7, 0.7, 0.7, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 80.0)

    return luz_pos

def calcular_normal(v1, v2, v3):
    # Cálculo do vetor normal para a face
    u = np.subtract(v2, v1)
    v = np.subtract(v3, v1)
    normal = np.cross(u, v)
    return normal / np.linalg.norm(normal)  # Normaliza a normal

def desenhar_cubo_unitario(luz_pos):
    hs = 0.5
    vertices = [
        [-hs, -hs, -hs], [hs, -hs, -hs], [hs, hs, -hs], [-hs, hs, -hs],  # Trás
        [-hs, -hs,  hs], [hs, -hs,  hs], [hs, hs,  hs], [-hs, hs,  hs]   # Frente
    ]
    faces = [
        [0, 1, 2, 3],  # Trás
        [4, 5, 6, 7],  # Frente
        [0, 1, 5, 4],  # Baixo
        [2, 3, 7, 6],  # Cima
        [0, 3, 7, 4],  # Esquerda
        [1, 2, 6, 5],  # Direita
    ]
    # Cores para demonstrar o efeito da luz, que vai mudar de acordo com a incidência da luz
    for i, face in enumerate(faces):
        v1, v2, v3 = vertices[face[0]], vertices[face[1]], vertices[face[2]]
        normal = calcular_normal(v1, v2, v3)

        # Vetor da luz (direção da luz)
        luz_dir = np.array(luz_pos[:3]) - np.array(v1)
        luz_dir = luz_dir / np.linalg.norm(luz_dir)  # Normaliza o vetor

        # Produto escalar entre a normal da face e a direção da luz
        intensidade = np.dot(normal, luz_dir)
        intensidade = np.clip(intensidade, 0, 1)  # A intensidade fica entre 0 e 1

        # Ajusta a cor dependendo da intensidade da luz
        cor = [intensidade, intensidade, intensidade]  # Escala a cor para a intensidade da luz

        glBegin(GL_QUADS)
        glColor3fv(cor)  # Aplique a cor com base na intensidade da luz
        for vert in face:
            glVertex3fv(vertices[vert])
        glEnd()

def desenhar_lampada(posicao):
    glPushMatrix()
    glTranslatef(*posicao[:3])
    glColor3f(1.0, 1.0, 0.2)

    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1.0, 1.0, 0.2, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 0.2, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 100.0)

    quad = gluNewQuadric()
    gluSphere(quad, 0.1, 20, 20)
    gluDeleteQuadric(quad)
    glPopMatrix()

def main():
    global rot_x, rot_y, angulo_luz
    window = init_window(800, 600, "Cubo com Iluminação Dinâmica e Luz Rotacionando")
    glEnable(GL_DEPTH_TEST)

    luz_pos = configurar_luz()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 100)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Atualiza a posição da luz, girando como o sol
        angulo_luz += 0.1  # Aumenta o ângulo da luz para fazer ela girar
        luz_pos = configurar_luz()  # Recalcula a posição da luz

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(4, 4, 6, 0, 0, 0, 0, 1, 0)

        # Aplica rotação com base no mouse
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        # Cubo central
        glPushMatrix()
        desenhar_cubo_unitario(luz_pos)
        glPopMatrix()

        # Lâmpada
        desenhar_lampada(luz_pos)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
