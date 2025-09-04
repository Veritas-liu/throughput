import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt

# 读取数据
df = pd.read_excel('Summary.xlsx')

# 分组
grouped = df.groupby(['Topo', 'dim'])

# 第一张图：size vs mlu
plt.figure(figsize=(8,6))
for (topo, dim), group in grouped:
  plt.plot(group['size'], group['mlu'], marker='o', label=f'{topo}-{dim}')
plt.xlabel('size')
plt.ylabel('mlu')
plt.title('Size vs MLU')
plt.legend()
plt.tight_layout()
plt.savefig('fig1_size_mlu.png')
plt.close()

# 第二张图：size vs eff
plt.figure(figsize=(8,6))
for (topo, dim), group in grouped:
  plt.plot(group['size'], group['eff'], marker='o', label=f'{topo}-{dim}')
plt.xlabel('size')
plt.ylabel('eff')
plt.title('Size vs Eff')
plt.legend()
plt.tight_layout()
plt.savefig('fig2_size_eff.png')
plt.close()

# 第三张图：size^dim vs eff
plt.figure(figsize=(8,6))
for (topo, dim), group in grouped:
  x = group['size'] ** group['dim']
  plt.plot(x, group['eff'], marker='o', label=f'{topo}-{dim}')
plt.xlabel('size^dim')
plt.ylabel('eff')
plt.title('Size^dim vs Eff')
plt.legend()
plt.tight_layout()
plt.savefig('fig3_sizedim_eff.png')
plt.close()

# 第四张图：Topo为Mesh的三维图（交互窗口）
mesh_df = df[df['Topo'] == 'mesh']
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')
x_mesh = mesh_df['size'] ** mesh_df['dim']
ax.scatter(x_mesh, mesh_df['dim'], mesh_df['eff'], c='b', marker='o')
ax.set_xlabel('size^dim')
ax.set_ylabel('dim')
ax.set_zlabel('eff')
ax.set_title('Mesh: size^dim, dim, eff')
plt.tight_layout()
plt.show()  # 展示交互窗口

# 第五张图：Topo为Turos的三维图（交互窗口）
turos_df = df[df['Topo'] == 'turos']
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')
x_turos = turos_df['size'] ** turos_df['dim']
ax.scatter(x_turos, turos_df['dim'], turos_df['eff'], c='r', marker='^')
ax.set_xlabel('size^dim')
ax.set_ylabel('dim')
ax.set_zlabel('eff')
ax.set_title('Turos: size^dim, dim, eff')
plt.tight_layout()
plt.show()  # 展示交互窗口
