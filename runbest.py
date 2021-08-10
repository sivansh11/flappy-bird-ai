import pipe
import color
import flappy
import random
import PyGameSetup as pg


showfps = False
# there are 5 inputs and 1 output
flappy.hidden_layer = [3]
flappy.output_above = 0.5
# flappy.nn.usefunc_hidden.set_functions(flappy.nn.sigmoid, flappy.nn.dsigmoid)
flappy.nn.debug = False

file = open('nn.p', 'rb')

bird = flappy.Bird(50, pg.height / 2, 20, pg.screen)
bird.brain.load(file)
file.close()
pipes = []

score = 0
font2 = pg.pygame.font.Font('freesansbold.ttf', 16)
text2 = font2.render(str(score), True, color.yellow)
text_rect2 = text2.get_rect()
text_rect2.center = (int(pg.width / 2), 150)

show = True
keytick = 10
frames_passed = 0
pressedframe = 0
high_score = 0
slow = True
run = True
while run:
    if slow:
        pg.clock.tick(pg.frame_rate)
    for event in pg.pygame.event.get():
        if event.type == pg.pygame.QUIT:
            run = False

    pg.screen.fill(color.black)

    for p in pipes:
        p.update()
    if frames_passed % 100 == 0 or len(pipes) == 0:  # VVV
        '''make sure a pipe is added before removing the last pipe and and the pipe is removed before the bird actully
           encounters the next pipe'''
        pipes.append(pipe.Pipe(pg.width, 0, 50, random.randint(25, 350), pg.screen, gap=200))
    if pipes[0].phy.position.x < -75:
        pipes.remove(pipes[0])  # increasing the score of the bird after removing the pipe
        score += 1

    if pipes[0].collision(bird):
        bird.dead = True

    if not bird.dead:
        if bird.phy.position.x + bird.r < pipes[0].phy.position.x:
            closestpipe = pipes[0]
        elif bird.phy.position.x < pipes[0].phy.position.x + pipes[0].w:
            closestpipe = pipes[0]
        else:
            closestpipe = pipes[1]
        if closestpipe.collision(bird):
            bird.dead = True
        bird.update()
        if pressedframe > 2:
            inputs = [bird.phy.velocity.y, bird.phy.position.y / pg.height, closestpipe.phy.position.x / pg.width,
                      bird.phy.position.y - (closestpipe.phy.position.y + closestpipe.h),
                      bird.phy.position.y - (closestpipe.phy.position.y + closestpipe.h + closestpipe.gap)]
            bird.think(inputs)
            pressedframe = 0
        else:
            pressedframe += 1

    else:
        bird.dead = True
        run = False


    if show:
        pg.screen.blit(text2, text_rect2)
        text2 = font2.render(str(score), True, color.yellow)

    keys = pg.pygame.key.get_pressed()
    if (keys[pg.pygame.K_SPACE] and show is not True) and keytick > 60:
        show = True
        keytick = 0
    if (keys[pg.pygame.K_SPACE] and show is True) and keytick > 60:
        show = False
        keytick = 0
    if (keys[pg.pygame.K_s] and slow is not True) and keytick > 60:
        slow = True
        keytick = 0
    if (keys[pg.pygame.K_s] and slow is True) and keytick > 60:
        slow = False
        keytick = 0
    keytick += 1

    if show:
        for p in pipes:
            p.show()

        if not bird.dead:
            bird.show()

    if showfps:
        fps = pg.clock.get_fps()
        print(fps)

    frames_passed += 1

    pg.pygame.display.update()
pg.pygame.quit()

