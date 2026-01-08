#化疗入院时间计算器
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import calendar

class ChemotherapyCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("化疗周期计算器")
        self.root.geometry("600x500")

        # 创建主框架
        main_frame = ttk.LabelFrame(root, text="输入治疗信息", padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 治疗日期 - 分为年月日三个输入框
        date_frame = ttk.Frame(main_frame)
        date_frame.pack(fill=tk.X, pady=5)

        ttk.Label(date_frame, text="治疗日期:").pack(side=tk.LEFT)

        self.year_entry = ttk.Entry(date_frame, width=8)
        self.year_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(date_frame, text="年").pack(side=tk.LEFT)

        self.month_entry = ttk.Entry(date_frame, width=8)
        self.month_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(date_frame, text="月").pack(side=tk.LEFT)

        self.day_entry = ttk.Entry(date_frame, width=8)
        self.day_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(date_frame, text="日").pack(side=tk.LEFT)

        # 周期数
        ttk.Label(main_frame, text="当前周期数:").pack(anchor=tk.W, pady=5)
        self.cycle_entry = ttk.Entry(main_frame, width=15)
        self.cycle_entry.pack(anchor=tk.W, padx=10, pady=5)

        # 间隔天数
        ttk.Label(main_frame, text="每周期间隔(天):").pack(anchor=tk.W, pady=5)
        self.interval_entry = ttk.Entry(main_frame, width=15)
        self.interval_entry.pack(anchor=tk.W, padx=10, pady=5)

        # 计算按钮
        calculate_btn = ttk.Button(main_frame, text="计算后续周期", command=self.calculate_cycles)
        calculate_btn.pack(pady=15)

        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="计算结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 创建Treeview显示结果
        columns = ('周期数', '治疗日期', '星期')
        self.tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=12)

        # 定义列标题
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def calculate_cycles(self):
        try:
            # 获取输入值
            year_str = self.year_entry.get().strip()
            month_str = self.month_entry.get().strip()
            day_str = self.day_entry.get().strip()
            current_cycle = int(self.cycle_entry.get().strip())
            interval_days = int(self.interval_entry.get().strip())

            # 验证输入是否为空
            if not (year_str and month_str and day_str):
                messagebox.showerror("输入错误", "请完整输入治疗日期的年、月、日")
                return

            # 转换为整数
            year = int(year_str)
            month = int(month_str)
            day = int(day_str)

            # 验证日期有效性
            try:
                treatment_date = datetime(year, month, day)
            except ValueError:
                messagebox.showerror("输入错误", "请输入有效的日期")
                return

            # 清空之前的计算结果
            for item in self.tree.get_children():
                self.tree.delete(item)

            # 计算接下来的10个周期
            for i in range(1, 11):
                cycle_num = current_cycle + i
                next_date = treatment_date + timedelta(days=i * interval_days)

                # 获取星期几
                weekday_cn = self.get_chinese_weekday(next_date.weekday())

                # 添加到Treeview
                self.tree.insert('', tk.END, values=(cycle_num, next_date.strftime('%Y-%m-%d'), weekday_cn))

        except ValueError as e:
            messagebox.showerror("输入错误", f"请输入正确的数字格式:\n周期数和间隔天数应为整数")
        except Exception as e:
            messagebox.showerror("错误", f"计算出错: {str(e)}")

    def get_chdinese_weekday(self, weekday_num):
        """将数字星期转换为中文"""
        weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return weekdays[weekday_num]

if __name__ == "__main__":
    root = tk.Tk()
    app = ChemotherapyCalculator(root)
    root.mainloop()
