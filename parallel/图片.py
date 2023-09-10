import matplotlib.pyplot as plt

# 示例数据
x = [1, 2, 3, 4, 5]
y1 = [1, 4, 9, 16, 25]
y2 = [1, 8, 27, 64, 125]

# 创建图表和坐标轴
fig, ax = plt.subplots()

# 绘制折线图
line1, = ax.plot(x, y1, label='Line 1')
line2, = ax.plot(x, y2, label='Line 2')

# 添加坐标轴标签
ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')

# 添加图例
ax.legend(loc='upper right')

# 显示图表
plt.show()