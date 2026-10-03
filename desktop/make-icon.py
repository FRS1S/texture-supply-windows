# Gera build/icon.png (512x512): placa preta, retícula verde-limão e o asterisco do piraru*.
import zlib, struct, math, os

S = 512
BLACK = (10, 10, 10)
LIME = (182, 255, 0)      # #B6FF00, cor do vídeo de abertura
R, M = 104, 20            # raio do canto, margem externa
CELL = 24                 # tamanho da célula da retícula
AST_C = (S * 0.69, S * 0.31)  # centro do asterisco
AST_L, AST_W = 62, 15     # meio-comprimento e meia-largura de cada braço


def sstep(a, b, x):
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


ARMS = []
for k in range(3):
    a = math.radians(90 + k * 60)
    ARMS.append((AST_C[0] - math.cos(a) * AST_L, AST_C[1] - math.sin(a) * AST_L,
                 AST_C[0] + math.cos(a) * AST_L, AST_C[1] + math.sin(a) * AST_L))


def asterisk(x, y):
    d = min(seg_dist(x, y, *arm) for arm in ARMS) - AST_W
    return d


px = bytearray(S * S * 4)
ang = math.radians(45)
ca, sa = math.cos(ang), math.sin(ang)
for y in range(S):
    for x in range(S):
        qx = max(M + R - x, 0, x - (S - M - R))
        qy = max(M + R - y, 0, y - (S - M - R))
        a = 1 - sstep(-0.8, 0.8, math.hypot(qx, qy) - R)
        if a <= 0:
            continue
        # retícula: pontos crescem em direção ao canto inferior esquerdo
        u = (x * ca + y * sa) / CELL
        v = (-x * sa + y * ca) / CELL
        fu, fv = u - math.floor(u) - .5, v - math.floor(v) - .5
        d = math.hypot(fu, fv) * CELL
        tone = max(0.0, min(1.0, 0.78 - math.hypot(x - S * 0.12, y - S * 0.9) / (S * 0.9)))
        r = CELL * 0.66 * math.sqrt(tone)
        dot = 1 - sstep(r - 0.9, r + 0.9, d)
        ad = asterisk(x, y)
        dot *= sstep(10, 13, ad)                # halo preto em volta do asterisco
        ink = max(dot, 1 - sstep(-0.9, 0.9, ad))  # asterisco sólido
        col = [BLACK[i] + (LIME[i] - BLACK[i]) * ink for i in range(3)]
        o = (y * S + x) * 4
        px[o:o + 4] = bytes([int(col[0]), int(col[1]), int(col[2]), int(a * 255)])


def chunk(t, d):
    return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)


raw = b''.join(b'\x00' + bytes(px[y * S * 4:(y + 1) * S * 4]) for y in range(S))
os.makedirs('build', exist_ok=True)
with open('build/icon.png', 'wb') as f:
    f.write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', S, S, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))
print('build/icon.png gerado')
