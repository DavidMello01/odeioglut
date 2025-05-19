import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

def init_window(width, height, title):
    if not glfw.init():
        raise Exception("GLFW não pôde ser inicializado")
    window = glfw.create_window(width, height, title, None, None)
    glfw.make_context_current(window)
    return window

def configurar_luz():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    # Posicionamento da luz
    luz_pos = [2.0, 2.0, 2.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, luz_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    # Material padrão da cena
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.7, 0.7, 0.7, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 80.0)

    return luz_pos  # Retorna a posição da luz para desenhar a "lâmpada"

def desenhar_lampada(posicao):
    glPushMatrix()
    glTranslatef(*posicao[:3])
    glColor3f(1.0, 1.0, 0.2)  # Cor amarelada

    # Material brilhante (simula emissão)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1.0, 1.0, 0.2, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 0.2, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 100.0)

    glutSolidSphere(0.1, 20, 20)
    glPopMatrix()

def main():
    glutInit()
    window = init_window(800, 600, "Lâmpada como Fonte de Luz")
    glEnable(GL_DEPTH_TEST)

    luz_pos = configurar_luz()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 100)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(4, 4, 6, 0, 0, 0, 0, 1, 0)

        # Rotacionar cena
        glRotatef(glfw.get_time() * 20, 0, 1, 0)

        # Cubo central
        glPushMatrix()
        glColor3f(0.5, 0.5, 0.5)
        glutSolidCube(1.0) #PQ NUYM TA RODANDOOOOOOOOOOOOOO 0X000000000000C1 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA maldito glut.
        glPopMatrix()

        # Desenhar a lâmpada
        desenhar_lampada(luz_pos)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
