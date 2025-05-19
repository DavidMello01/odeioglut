import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutInit, glutSolidCube, glutSolidSphere
import numpy as np

def init_window(width, height, title):
    if not glfw.init():
        raise Exception("GLFW não pôde ser inicializado")
    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception("Janela GLFW não pôde ser criada")
    glfw.make_context_current(window)
    return window

def iluminar():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 2.0, 2.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.6, 0.6, 0.6, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 80.0)

def desenhar_cubo_arredondado():
    size = 1.0
    r = 0.2
    steps = 20

    glPushMatrix()
    glScalef(size - 2*r, size - 2*r, size - 2*r)
    glutSolidCube(1.0)
    glPopMatrix()

    for dx in [-1, 1]:
        for dy in [-1, 1]:
            for dz in [-1, 1]:
                glPushMatrix()
                glTranslatef(dx*(size/2 - r), dy*(size/2 - r), dz*(size/2 - r))
                glutSolidSphere(r, steps, steps)
                glPopMatrix()

    def cilindro_entre(p1, p2):
        dir = np.array(p2) - np.array(p1)
        length = np.linalg.norm(dir)
        if length == 0:
            return
        dir = dir / length

        angle = np.arccos(np.dot(dir, [0, 0, 1])) * 180 / np.pi
        axis = np.cross([0, 0, 1], dir)
        glPushMatrix()
        glTranslatef(*p1)
        if np.linalg.norm(axis) > 0:
            glRotatef(angle, *axis)
        quad = gluNewQuadric()
        gluCylinder(quad, r, r, length, steps, 1)
        gluDeleteQuadric(quad)
        glPopMatrix()

    pontos = [-1, 1]
    arestas = []
    for x in pontos:
        for y in pontos:
            for z in pontos:
                if x == -1:
                    arestas.append(((x*(size/2 - r), y*(size/2 - r), z*(size/2 - r)),
                                    ((x+2)*(size/2 - r), y*(size/2 - r), z*(size/2 - r))))
                if y == -1:
                    arestas.append(((x*(size/2 - r), y*(size/2 - r), z*(size/2 - r)),
                                    (x*(size/2 - r), (y+2)*(size/2 - r), z*(size/2 - r))))
                if z == -1:
                    arestas.append(((x*(size/2 - r), y*(size/2 - r), z*(size/2 - r)),
                                    (x*(size/2 - r), y*(size/2 - r), (z+2)*(size/2 - r))))
    for a, b in arestas:
        cilindro_entre(a, b)

def main():
    glutInit()  
    window = init_window(800, 600, "Cubo de Inox com Cantos Arredondados")
    
    glEnable(GL_DEPTH_TEST)
    iluminar()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 100)

    rot_x, rot_y = 0, 0

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(3, 3, 4, 0, 0, 0, 0, 1, 0)

        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        desenhar_cubo_arredondado()

        rot_x += 0.3
        rot_y += 0.4

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
