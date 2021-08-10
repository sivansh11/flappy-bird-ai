import pipe
import color
import flappy
import random
import PyGameSetup as pg
from nn import crossover


showfps = False
showgenstats = True
pop = 150
mutation_rate = 0.015
crossoverrate = 0.2
mutation_limit = -0.01, 0.01
# there are 5 inputs and 1 output
flappy.hidden_layer = [3]
flappy.output_above = 0.5
# flappy.nn.usefunc_hidden.set_functions(flappy.nn.sigmoid, flappy.nn.dsigmoid)
flappy.nn.debug = False
new = 5  # in percentage
score_limit = 2000

file = open('nn.p', 'wb')


class Population:
    def __init__(self, size):
        self.size = size
        self.list = []
        for i in range(self.size):
            self.list.append(flappy.Bird(50, pg.height / 2, 20, pg.screen))
        self.fitlist = []

    def fitness(self):
        biggest = 0
        biggest_brain = None
        for bird in self.list:
            if bird.score > biggest:
                biggest = bird.score
                biggest_brain = bird.brain
        #
        # file.seek(0)
        # biggest_brain.save(file)

        for bird in self.list:
            bird.score = int((bird.score / biggest) * 100)


    def selection(self):
        matingpool = []
        for bird in self.list:
            for i in range(bird.score):
                matingpool.append(bird)

        self.list.clear()
        matinglen = len(matingpool) - 1
        v = None

        new_species = int((new / 100) * self.size)

        for i in range(self.size - new_species):
            if score <= high_score:
                parent1 = matingpool[random.randint(0, matinglen)]
                parent2 = matingpool[random.randint(0, matinglen)]
                child = flappy.Bird(50, pg.height / 2, 20, pg.screen)
                child.brain = crossover(parent1.brain, parent2.brain, crossoverrate)
                child.color = flappy.newcol(parent1.color, parent2.color)
            else:
                parent = matingpool[random.randint(0, matinglen)]
                child = flappy.Bird(50, pg.height / 2, 20, pg.screen)
                child.brain = parent.brain
                child.color = parent.color
            child.brain.mutate(mutation_rate, mutation_limit)
            self.list.append(child)

        for i in range(new_species):
            self.list.append(flappy.Bird(50, pg.height / 2, 20, pg.screen))


birds = Population(pop)
pipes = []

noalive = pop
font = pg.pygame.font.Font('freesansbold.ttf', 16)
text = font.render(str(noalive), True, color.yellow)
text_rect = text.get_rect()
text_rect.center = (int(pg.width / 2), 100)

score = 0
font2 = pg.pygame.font.Font('freesansbold.ttf', 16)
text2 = font.render(str(score), True, color.yellow)
text_rect2 = text.get_rect()
text_rect2.center = (int(pg.width / 2), 150)

generation = 0
font3 = pg.pygame.font.Font('freesansbold.ttf', 16)
text3 = font.render(str(generation), True, color.yellow)
text_rect3 = text.get_rect()
text_rect3.center = (int(pg.width / 2), 50)

curr_fps = 0
font4 = pg.pygame.font.Font('freesansbold.ttf', 16)
text4 = font.render(str(generation), True, color.white)
text_rect4 = text.get_rect()
text_rect4.center = (int(pg.width - 20), 10)

alldead = False
show = True
keytick = 10
frames_passed = 0
pressedframe = 0
high_score = 0
forcenew = False
slow = True
run = True
fps = 60
while run:
    pg.clock.tick(fps)
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
    for bird in birds.list:
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
            if bird.score > score_limit:
                run = False
                bird.brain.save(file)
                file.close()
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

    noalive = 0
    alldead = True
    for bird in birds.list:
        if bird.dead is False:
            alldead = False
            noalive += 1

    if alldead:
        forcenew = True
        if score > high_score:
            high_score = score

        birds.fitness()
        birds.selection()
        pipes.clear()
        alldead = False
        frames_passed = 0
        noalive = pop
        if score > high_score:
            high_score = score
        if showgenstats:
            print('Generation:', generation, '  Score:',score, '  High Score:', high_score)
        generation += 1

        score = 0

    if show:
        pg.screen.blit(text, text_rect)
        text = font.render(str(noalive), True, color.purple)

        pg.screen.blit(text2, text_rect2)
        text2 = font.render(str(score), True, color.yellow)

        pg.screen.blit(text3, text_rect3)
        text3 = font.render(str(generation), True, color.white)


        curr_fps = int(pg.clock.get_fps())

        pg.screen.blit(text4, text_rect4)
        text4 = font.render(str(curr_fps), True, color.white)

    keys = pg.pygame.key.get_pressed()
    if (keys[pg.pygame.K_SPACE] and show is not True) and keytick > 60:
        show = True
        keytick = 0
    if (keys[pg.pygame.K_SPACE] and show is True) and keytick > 60:
        show = False
        keytick = 0
    if (keys[pg.pygame.K_s] and slow is not True) and keytick > 60:
        slow = True
        fps = 60
        keytick = 0
    if (keys[pg.pygame.K_s] and slow is True) and keytick > 60:
        slow = False
        fps = 10000000
        keytick = 0
    if keys[pg.pygame.K_UP] and keytick > 60:
        fps += 10
        keytick = 0
    if keys[pg.pygame.K_DOWN] and keytick > 60:
        fps -= 10
        keytick = 0
    keytick += 1

    if show:
        for p in pipes:
            p.show()
        for bird in birds.list:
            if not bird.dead:
                bird.show()

    if showfps:
        curr_fps = pg.clock.get_fps()
        print(curr_fps)

    frames_passed += 1

    pg.pygame.display.update()
pg.pygame.quit()

