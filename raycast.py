import pygame 
import math
import sys

FOV=math.pi/3
HALF_FOV=FOV/2
SCREEN_HEIGHT=480
SCREEN_WIDTH=SCREEN_HEIGHT*2
TILE_SIZE=int((SCREEN_HEIGHT/2)/8)
M_T=8

CASTED_RAYS=160
DEPTH=int(M_T*TILE_SIZE)
SCALE = ((SCREEN_WIDTH /2) / CASTED_RAYS) +2




p_x = 200 
p_y = 200
p_a=math.pi


light_grey = (191, 191, 191)
dark_grey = (65, 65, 65)
red=(123,123,123)

MAP=  ('########'
       '# #    #'    
       '# #  # #'    
       '#      #'   
       '##     #'   
       '#  ### #'   
       '#   #  #'  
       '########')


pygame.init()
window=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Ray-Caster")
clock=pygame.time.Clock()

def draw_map():
    for i in range(M_T):
        for j in range(M_T):
            sq=i*M_T+j  
            pygame.draw.rect(window,light_grey if MAP[sq]=='#' else dark_grey,(j*TILE_SIZE,i*TILE_SIZE,TILE_SIZE-1,TILE_SIZE-1))
    pygame.draw.circle(window,(0,0,0),(int(p_x),int(p_y)),7)


def raycast():
    start_angle=p_a-HALF_FOV
    for i in range(CASTED_RAYS):
        for j in range(DEPTH):
            t_x=p_x-math.sin(start_angle)*j #gives the target coords for x or where the ray should end
            t_y=p_y+math.cos(start_angle)*j #gives the target coords for y or where the ray should end
            
            col=int(t_x/TILE_SIZE) #convert to map coords
            row=int(t_y/TILE_SIZE)

            square=row*M_T +col #map sq indx
            if 0<=col<M_T and 0<=row<M_T:
                if MAP[square]=='#':
                    pygame.draw.rect(window, (195, 137, 38), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))  

                    pygame.draw.line(window,'white',(p_x,p_y),(t_x,t_y))

                    color = 255 / (1 + j * j* 0.0001) #depth

                    j*= math.cos(p_a - start_angle) #fisheye

                    wall_height = 21000 / (j)

                    if wall_height>SCREEN_HEIGHT:
                        wall_height=SCREEN_HEIGHT

                    pygame.draw.rect(window,(color,color,color),(SCREEN_HEIGHT*0.5 + i* SCALE, (SCREEN_HEIGHT / 2) - wall_height / 2, SCALE, wall_height))

                    break
        start_angle+=(FOV/CASTED_RAYS) # at what angle to make the next line




#movement direction
forward=True


while True:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    pygame.draw.rect(window, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

    pygame.draw.rect(window, (0, 0, 0), (480, SCREEN_HEIGHT/2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    pygame.draw.rect(window, (0,0,0), (480, -SCREEN_HEIGHT /2, SCREEN_HEIGHT, SCREEN_HEIGHT))

    draw_map()
    raycast()

    #fps display
    fps=str(int(clock.get_fps()))
    font=pygame.font.SysFont('Arial',20)
    fp_disp=font.render(f"FPS: {fps}",False,(255,255,255))
    window.blit(fp_disp,(int(SCREEN_WIDTH*0.02),SCREEN_HEIGHT*0.5))


    #player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        #working with radians, not degrees
        p_a -= 0.1
    elif keys[pygame.K_RIGHT]:
        p_a += 0.1
    elif keys[pygame.K_UP]:
        forward = True
        p_x += -1 * math.sin(p_a) * 5
        p_y += math.cos(p_a) * 5
    elif keys[pygame.K_DOWN]:
        forward = False
        p_x -= -1 * math.sin(p_a) * 5
        p_y -= math.cos(p_a) * 5

    #collision detection
    r=int(p_y/TILE_SIZE)
    c=int(p_x/TILE_SIZE)
    sq=r*M_T+c
    if MAP[sq]=='#':
        if forward:
            p_x-=-1*math.sin(p_a)*5
            p_y-=math.cos(p_a)*5
        else:
            p_x_x += -1 * math.sin(p_a) * 5
            p_x_y += math.cos(p_a) * 5

    pygame.display.flip()
    clock.tick(30)

