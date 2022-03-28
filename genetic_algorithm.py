import random 
import numpy as np

def gen_individual(length): # length = target length
    genes = []
    while len(genes) < length:
        sampleSize = min(length - len(genes), len(geneSet)) # 작은 길이 고르는건데 이게 geneSet 보다 길면 안된다는거지 그래야 sampling 할 수 있으니까 # 만약 길이 더 길면 geneSet 길이 만큼만 sampling
        genes.extend(random.sample(geneSet, sampleSize)) # geneSet 에서 sampleSize 만큼 sampling' # sampleSize 번 반복해서 geneSet에서 sampling 한다 # return sampleSize 길이의 배열 

        return ''.join(genes) # 리스트 요소들을 합쳐서 문자열로 반환
    
def get_fitness(guess, target):
    return sum(1 for expected, actual in zip(target, guess) if expected == actual) # targe과 guess 리스트에서 같은 값일 때마다 1을 더함

# def mutate(parent): # child 의 index 값 하나 바꾸는 함수 ## child 를 매개변수로 받아야 함 ## parent로 만들어진 결과를 받아야지 
#     index = random.randrange(0, len(parent)) # parent compound 할 때 기준 설정 # 합치는 기준 인덱스 설정 
#     childGenes = list(parent) ## child 로 수정돼야 함
#     ## ramdom probability로 mutate 실행하는 걸로 수정
#     newGene, alternate = random.sample(geneSet, 2) 
#     childGenes[index] = alternate if newGene == childGenes[index] else newGene

# 3 주어진 코드의 mutate 함수를 이용하여 생성된 자녀를 변이 시킵니다. 
# 바꿀 인덱스와 알파벳을 랜덤으로 정해 바꿔준다
def mutate(child):
    index = random.randrange(0, len(child))
    childGenes = list(child)
    alternate = ''.join(random.sample(geneSet, 1))
    childGenes[index] = alternate
    return ''.join(childGenes)

def display(guess, fitness):
    print("{}\t{}".format(guess, fitness)) # {guess}    {fitness} 형태로 출력
    
def reproduce(x, y):
    re_parent = []
    n = len(x)
    c = random.randrange(1, n) # 1이상 n미만
    x_sub = x[0:c]
    y_sub = y[c:n]
    re_parent.extend(x_sub) # 자른 x_sub 뒤에 y_sub 붙여준다
    re_parent.extend(y_sub)

    return re_parent    

###################
# 2 룰렛휠 방식으로 부모를 선택하여 새로운 자녀를 생성합니다. 
# guesses 여러개 받아서 그 중 나은 guess 뽑아 내야 함

def random_selection(population, target):
    population_fitness = sum([get_fitness(guess, target) for guess in population])
    guess_probabilities = [get_fitness(guess, target) / population_fitness for guess in population]

    return np.random.choice(population, p = guess_probabilities)


if __name__ == "__main__" :
    geneSet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.'
    target = 'bear'

    # population 생성
    # len_population = 500 
    len_population = 500 # 1 population의 수는 500 정도가 적당합니다.
    population = []
    population_probability = 0
    
    # 4 과정을 약 100 세대동안 반복하세요. 
    for i in range(100):
        new_population = []

        if i != 0 :
            fitness = [get_fitness(guess, target) for guess in population]
            best_fitness = max(fitness)
            best_index = fitness.index(best_fitness)
            best = population[best_index]
            print("{}\t{}".format(best, best_fitness))
            if best == target:
                break         
        # while population_probability == 0: # probability 0 이 아닐 때까지 poulation 재생성
        for j in range(len_population):
            gen_individual(len(target)) 
            population.append(gen_individual(len(target)))
            population_probability = sum([get_fitness(guess, target) for guess in population])
            
        for j in range(len_population):
            x = random_selection(population, target)
            y = random_selection(population, target)
            child = reproduce(x, y)
            
            mutate_probability = random.randrange(0, 1)
            if mutate_probability < 0.5 :
                child = mutate(list(child))
            new_population.append(child)
                         
        population = new_population