import subprocess
import os
import concurrent.futures

test_case = [('mesh', 2, i) for i in range(2, 9)] + \
            [('turos', 2, i) for i in range(3, 9)] + \
            [('mesh', 3, i) for i in range(2, 5)] + \
            [('turos', 3, i) for i in range(3, 5)]
# Stage 1: 编译 genpath 和 gentopo
print('Compiling genpath and gentopo...')
subprocess.run(['g++', 'genpath.cpp', '-o', 'genpath'])
subprocess.run(['g++', 'gentopo.cpp', '-o', 'gentopo'])

# Stage 2: gentopo 并行执行
print('Generating topologies...')
with concurrent.futures.ThreadPoolExecutor() as executor:
  futures = [
    executor.submit(
      subprocess.run,
      ['./gentopo', '--topo', topo, '--dim', str(n), '--size', str(m)]
    )
    for topo, n, m in test_case
  ]
concurrent.futures.wait(futures)

# Stage 3: 生成路径 (已顺序执行)
print('Generating paths...')
subprocess.run(['./genpath'])

# Stage 4: solve.py 并行执行
print('Solving MLU...')
with concurrent.futures.ThreadPoolExecutor() as executor:
  futures = [
    executor.submit(
      subprocess.run,
      ['python', 'solve.py', f'{topo}_{n}d_{m}']
    )
    for topo, n, m in test_case
  ]
concurrent.futures.wait(futures)

log_dir = './log'
print('Summary:')
for filename in os.listdir(log_dir):
  if filename.endswith('.log'):
    filepath = os.path.join(log_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
      lines = f.readlines()
      if lines:
        a = lines[-1].strip().split()[-2:]
        print(f'{a[0]}: {a[1]}')