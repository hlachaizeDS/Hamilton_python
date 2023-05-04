path2 = r'C:\Users\Martin\OneDrive - DNA Script\Documents\H_Simu\Cycle.txt'


def getCycle(path2):

    with open(path2) as f:
        cycle = f.readlines()
    return cycle[1]

def writeCycle(path2,cycle):
    f = open(path2, 'w')
    f.write('Cycle' + '\n' + str(cycle))
    f.close()



