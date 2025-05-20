import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
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

def desenhar_cubo_unitario():
    # Desenha um cubo unitário centrado na origem usando GL_QUADS
    hs = 0.5  # Half size
    vertices = [
        [-hs, -hs, -hs], [hs, -hs, -hs], [hs, hs, -hs], [-hs, hs, -hs],  # Traseira
        [-hs, -hs, hs], [hs, -hs, hs], [hs, hs, hs], [-hs, hs, hs]       # Frontal
    ]
    faces = [
        [0, 1, 2, 3],  # Traseira
        [4, 5, 6, 7],  # Frontal
        [0, 1, 5, 4],  # Inferior
        [2, 3, 7, 6],  # Superior
        [0, 3, 7, 4],  # Esquerda
        [1, 2, 6, 5],  # Direita
    ]
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def desenhar_cubo_arredondado():
    size = 1.0
    r = 0.2
    steps = 20

    # Cubo central
    glPushMatrix()
    glScalef(size - 2*r, size - 2*r, size - 2*r)
    desenhar_cubo_unitario()
    glPopMatrix()

    # Esferas nos cantos
    quad = gluNewQuadric()
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            for dz in [-1, 1]:
                glPushMatrix()
                glTranslatef(dx*(size/2 - r), dy*(size/2 - r), dz*(size/2 - r))
                gluSphere(quad, r, steps, steps)
                glPopMatrix()

    # Cilindros entre os cantos
    def cilindro_entre(p1, p2):
        dir = np.array(p2) - np.array(p1)
        length = np.linalg.norm(dir)
        if length == 0:
            return
        dir = dir / length
        angle = np.degrees(np.arccos(np.dot(dir, [0, 0, 1])))
        axis = np.cross([0, 0, 1], dir)
        glPushMatrix()
        glTranslatef(*p1)
        if np.linalg.norm(axis) > 0:
            glRotatef(angle, *axis)
        gluCylinder(gluNewQuadric(), r, r, length, steps, 1)
        glPopMatrix()

    pontos = [-1, 1]
    for x in pontos:
        for y in pontos:
            for z in pontos:
                cx = x * (size/2 - r)
                cy = y * (size/2 - r)
                cz = z * (size/2 - r)
                if x == -1:
                    cilindro_entre((cx, cy, cz), (cx + size - 2*r, cy, cz))
                if y == -1:
                    cilindro_entre((cx, cy, cz), (cx, cy + size - 2*r, cz))
                if z == -1:
                    cilindro_entre((cx, cy, cz), (cx, cy, cz + size - 2*r))
    gluDeleteQuadric(quad)

def main():
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
