import tkinter as tk
import numpy as np
import time


def get_mn_num_models():
    m = int(input('请输入行数'))
    n = int(input('请输入列数'))
    num_models = int(input('请输入模块数'))
    return m, n, num_models


def get_model(m, n, model_list, num, m_list, n_list):

    def get_matrix_model():
        matrix = np.zeros((m, n))
        for i in range(m):
            for j in range(n):
                if entry_list[n * i + j].get() == '1':
                    matrix[i, j] = 1

        for i in range(m):
            sum = 0
            for j in range(n):
                sum += matrix[i, j]
            if sum > 0:
                i_min = i
                break
        for i in range(m):
            sum = 0
            for j in range(n):
                sum += matrix[m - 1 - i, j]
            if sum > 0:
                i_max = m - 1 - i
                break
        for j in range(n):
            sum = 0
            for i in range(m):
                sum += matrix[i, j]
            if sum > 0:
                j_min = j
                break
        for j in range(n):
            sum = 0
            for i in range(m):
                sum += matrix[i, n - 1 - j]
            if sum > 0:
                j_max = n - 1 - j
                break

        m_r = i_max - i_min + 1
        n_r = j_max - j_min + 1

        matrix_r = np.zeros((m_r, n_r))
        for i in range(m_r):
            for j in range(n_r):
                matrix_r[i, j] = matrix[i + i_min, j + j_min]

        model_list.append(matrix_r)
        m_list.append(m_r)
        n_list.append(n_r)
        # print(matrix_r)
        # print(m_r, n_r)
        root.destroy()


    root = tk.Tk()
    root.geometry("{}x{}".format(30 * n + 150, 30 * m))
    root.title("模块输入{}".format(num + 1))
    root.resizable(False, False)

    entry_list = []
    stringvar_list = []

    for i in range(n * m):
        stringvar_list.append(tk.StringVar())
        stringvar_list[i].set('')
        entry_list.append(tk.Entry(root, textvariable=stringvar_list[i], width=3))

    for i in range(m):
        for j in range(n):
            entry_list[n * i + j].place(x=30 * j + 50, y=30 * i)

    tk.Button(root, text="确认", command=get_matrix_model).place(x=30 * n + 75, y=15 * m)
    root.mainloop()

def target(m, n, num_models, model_list, m_list, n_list, target_filled_matrix, target_number_matrix, target_row_list, target_column_list, colors):
    entry_list = []
    stringvar_list = []

    entry_row_list = []
    stringvar_row_list = []
    entry_column_list = []
    stringvar_column_list = []

    def get_matrix_target():
        start = time.time()
        for i in range(m):
            for j in range(n):
                if entry_list[n * i + j].get() == '1':
                    target_filled_matrix[i, j] = 1
                    target_number_matrix[i, j] = 1
                elif entry_list[n * i + j].get() == '0':
                    target_filled_matrix[i, j] = 1
        for i in range(m):
            target_row_list[i] = entry_row_list[i].get()
        for j in range(n):
            target_column_list[j] = entry_column_list[j].get()
        # print(target_filled_matrix, target_number_matrix, target_row_list, target_column_list)

        def rotation(matrix, m, n):
            m_r = n
            n_r = m
            matrix_r = np.zeros((m_r, n_r))
            for i in range(m_r):
                for j in range(n_r):
                    matrix_r[i, j] = matrix[m - 1 - j, i]
            return matrix_r

        model_list_1 = []
        m_list_1 = []
        n_list_1 = []
        model_list_2 = []
        m_list_2 = []
        n_list_2 = []
        model_list_3 = []
        m_list_3 = []
        n_list_3 = []
        for num in range(num_models):
            model_list_1.append(rotation(model_list[num], m_list[num], n_list[num]))
            m_list_1.append(n_list[num])
            n_list_1.append(m_list[num])
        for num in range(num_models):
            model_list_2.append(rotation(model_list_1[num], m_list_1[num], n_list_1[num]))
            m_list_2.append(m_list[num])
            n_list_2.append(n_list[num])
        for num in range(num_models):
            model_list_3.append(rotation(model_list_2[num], m_list_2[num], n_list_2[num]))
            m_list_3.append(n_list[num])
            n_list_3.append(m_list[num])

        solved = False
        for direction in range(4 ** num_models):
            if solved:
                break
            choose_direction = []
            matrix_choose = []
            m_choose = []
            n_choose = []
            for num in range(num_models):
                choose_direction.append(direction % 4)
                direction = direction // 4
            for num in range(num_models):
                if choose_direction[num] == 0:
                    matrix_choose.append(model_list[num])
                    m_choose.append(m_list[num])
                    n_choose.append(n_list[num])
                elif choose_direction[num] == 1:
                    matrix_choose.append(model_list_1[num])
                    m_choose.append(m_list_1[num])
                    n_choose.append(n_list_1[num])
                elif choose_direction[num] == 2:
                    matrix_choose.append(model_list_2[num])
                    m_choose.append(m_list_2[num])
                    n_choose.append(n_list_2[num])
                elif choose_direction[num] == 3:
                    matrix_choose.append(model_list_3[num])
                    m_choose.append(m_list_3[num])
                    n_choose.append(n_list_3[num])

            total_moves = 1
            move_able = True
            for num in range(num_models):
                if m - m_choose[num] >= 0:
                    total_moves *= (m - m_choose[num] + 1)
                else:
                    move_able = False
                    break
                if n - n_choose[num] >= 0:
                    total_moves *= (n - n_choose[num] + 1)
                else:
                    move_able = False
                    break

            if move_able:
                m_move = []
                n_move = []
                m_move_max = []
                n_move_max = []
                for num in range(num_models):
                    m_move.append(0)
                    n_move.append(0)
                    m_move_max.append(m - m_choose[num] + 1)
                    n_move_max.append(n - n_choose[num] + 1)

                for move in range(total_moves):
                    m_move[0] += 1

                    if solved:
                        break
                    non_repeat = True
                    target_filled_calc = np.zeros((m, n))
                    target_number_calc = np.zeros((m, n))
                    for i in range(m):
                        for j in range(n):
                            target_filled_calc[i, j] = target_filled_matrix[i, j]
                            target_number_calc[i, j] = target_number_matrix[i, j]

                    for num in range(num_models):
                        if not non_repeat:
                            break
                        if m_move[num] >= m_move_max[num]:
                            m_move[num] = 0
                            n_move[num] += 1
                            if n_move[num] >= n_move_max[num]:
                                n_move[num] = 0
                                m_move[num + 1] += 1

                        for i in range(m_choose[num]):
                            if not non_repeat:
                                break
                            for j in range(n_choose[num]):
                                if not non_repeat:
                                    break
                                if matrix_choose[num][i, j] == 1:
                                    if target_filled_calc[m_move[num] + i, n_move[num] + j] >= 1:
                                        non_repeat = False
                                        break
                                    target_number_calc[m_move[num] + i, n_move[num] + j] += 1
                                    target_filled_calc[m_move[num] + i, n_move[num] + j] += 1

                    if non_repeat:
                        solved = True
                        for i in range(m):
                            sum = 0
                            for j in range(n):
                                sum += target_number_calc[i, j]
                            if sum != target_row_list[i]:
                                solved = False
                                break

                        for j in range(n):
                            sum = 0
                            for i in range(m):
                                sum += target_number_calc[i, j]
                            if sum != target_column_list[j]:
                                solved = False
                                break


                        if solved:
                            for num in range(num_models):
                                for i in range(m_choose[num]):
                                    for j in range(n_choose[num]):
                                        if matrix_choose[num][i, j] == 1:
                                            entry_list[n * (m_move[num] + i) + (n_move[num] + j)]['background'] = colors[num]
                            end = time.time()
                            print(end - start)


    root = tk.Tk()
    root.geometry("{}x{}".format(30 * (n + 1) + 150, 30 * (m + 1)))
    root.title("目标输入")
    root.resizable(False, False)


    for i in range(n * m):
        stringvar_list.append(tk.StringVar())
        stringvar_list[i].set('')
        entry_list.append(tk.Entry(root, textvariable=stringvar_list[i], width=3))

    for i in range(m):
        stringvar_row_list.append(tk.StringVar())
        stringvar_row_list[i].set('0')
        entry_row_list.append(tk.Entry(root, textvariable=stringvar_row_list[i], width=3))
    for j in range(n):
        stringvar_column_list.append(tk.StringVar())
        stringvar_column_list[j].set('0')
        entry_column_list.append(tk.Entry(root, textvariable=stringvar_column_list[j], width=3))

    for i in range(m):
        for j in range(n):
            entry_list[n * i + j].place(x=30 * j + 80, y=30 * i + 30)

    for i in range(m):
        entry_row_list[i].place(x=50, y=30 * i + 30)
    for j in range(n):
        entry_column_list[j].place(x=30 * j + 80, y=0)


    tk.Button(root, text="确认", command=get_matrix_target).place(x=30 * n + 105, y=15 * m)
    root.mainloop()



def main():
    m, n, num_models= get_mn_num_models()

    model_list = []
    m_list = []
    n_list = []
    target_filled_matrix = np.zeros((m, n))
    target_number_matrix = np.zeros((m, n))
    target_row_list = np.zeros(m)
    target_column_list = np.zeros(n)
    colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']

    for num in range(num_models):
        get_model(m, n, model_list, num, m_list, n_list)

    target(m, n, num_models, model_list, m_list, n_list, target_filled_matrix, target_number_matrix, target_row_list, target_column_list, colors)





if __name__ == '__main__':
    main()