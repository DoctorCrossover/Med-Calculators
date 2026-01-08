###化疗剂量计算器 ctrl+a复制
import tkinter as tk
from tkinter import ttk, messagebox
import math

class DoseCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("化疗计量计算器")
        self.root.geometry("700x600")

        # 创建选项卡
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 普通化疗药计算器选项卡
        self.normal_tab = ttk.Frame(notebook)
        notebook.add(self.normal_tab, text="普通化疗药")
        self.create_normal_dose_calculator()

        # 卡铂剂量计算器选项卡
        self.carboplatin_tab = ttk.Frame(notebook)
        notebook.add(self.carboplatin_tab, text="卡铂剂量")
        self.create_carboplatin_calculator()

    def create_normal_dose_calculator(self):
        """创建普通化疗药计算器界面"""
        # 输入框架
        input_frame = ttk.LabelFrame(self.normal_tab, text="输入患者信息", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # 身高输入
        ttk.Label(input_frame, text="身高 (cm):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.height_entry = ttk.Entry(input_frame, width=15)
        self.height_entry.grid(row=0, column=1, padx=5, pady=5)

        # 体重输入
        ttk.Label(input_frame, text="体重 (kg):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.weight_entry = ttk.Entry(input_frame, width=15)
        self.weight_entry.grid(row=1, column=1, padx=5, pady=5)

        # 药物剂量输入
        ttk.Label(input_frame, text="药物剂量 (mg/m²):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.dose_entry = ttk.Entry(input_frame, width=15)
        self.dose_entry.grid(row=2, column=1, padx=5, pady=5)

        # 计算按钮
        calc_btn = ttk.Button(input_frame, text="计算剂量", command=self.calculate_normal_dose)
        calc_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # 结果显示
        result_frame = ttk.LabelFrame(self.normal_tab, text="计算结果", padding=10)
        result_frame.pack(fill=tk.X, padx=10, pady=5)

        self.normal_result_label = ttk.Label(result_frame, text="", justify=tk.LEFT)
        self.normal_result_label.pack()

        # 公式显示
        formula_frame = ttk.LabelFrame(self.normal_tab, text="计算公式", padding=10)
        formula_frame.pack(fill=tk.X, padx=10, pady=5)

        formula_text = (
            "体表面积计算（中国通用公式）：\n"
            "BSA (m²) = 0.0061 × 身高(cm) + 0.0124 × 体重(kg) - 0.0099\n\n"
            "药物用量计算：\n"
            "用量(mg) = BSA × 药物剂量(mg/m²)\n"
            "用量(g) = 用量(mg) / 1000"
        )
        ttk.Label(formula_frame, text=formula_text, justify=tk.LEFT).pack(anchor=tk.W)

    def create_carboplatin_calculator(self):
        """创建卡铂剂量计算器界面"""
        # 输入框架
        input_frame = ttk.LabelFrame(self.carboplatin_tab, text="输入患者信息", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # AUC输入
        ttk.Label(input_frame, text="AUC:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.auc_entry = ttk.Entry(input_frame, width=15)
        self.auc_entry.grid(row=0, column=1, padx=5, pady=5)

        # 血肌酐输入
        ttk.Label(input_frame, text="血肌酐 (μmol/L):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.creatinine_entry = ttk.Entry(input_frame, width=15)
        self.creatinine_entry.grid(row=1, column=1, padx=5, pady=5)

        # 年龄输入
        ttk.Label(input_frame, text="年龄 (岁):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.age_entry = ttk.Entry(input_frame, width=15)
        self.age_entry.grid(row=2, column=1, padx=5, pady=5)

        # 体重输入
        ttk.Label(input_frame, text="体重 (kg):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.weight_entry_carbo = ttk.Entry(input_frame, width=15)
        self.weight_entry_carbo.grid(row=3, column=1, padx=5, pady=5)

        # 性别选择
        ttk.Label(input_frame, text="性别:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.gender_var = tk.StringVar(value="男")
        gender_frame = ttk.Frame(input_frame)
        gender_frame.grid(row=4, column=1, padx=5, pady=5)
        ttk.Radiobutton(gender_frame, text="男", variable=self.gender_var, value="男").pack(side=tk.LEFT)
        ttk.Radiobutton(gender_frame, text="女", variable=self.gender_var, value="女").pack(side=tk.LEFT)

        # 计算按钮
        calc_btn = ttk.Button(input_frame, text="计算卡铂剂量", command=self.calculate_carboplatin_dose)
        calc_btn.grid(row=5, column=0, columnspan=2, pady=10)

        # 结果显示
        result_frame = ttk.LabelFrame(self.carboplatin_tab, text="计算结果", padding=10)
        result_frame.pack(fill=tk.X, padx=10, pady=5)

        self.carboplatin_result_label = ttk.Label(result_frame, text="", justify=tk.LEFT)
        self.carboplatin_result_label.pack()

        # 公式显示
        formula_frame = ttk.LabelFrame(self.carboplatin_tab, text="计算公式", padding=10)
        formula_frame.pack(fill=tk.X, padx=10, pady=5)

        formula_text = (
            "男性肌酐清除率计算（Cockcroft-Gault公式）：\n"
            "男性肌酐清除率(ml/min) = [(140-年龄) × 体重] / [72 × 血清肌酐(mg/dL)]\n\n"
            "血清肌酐单位换算：\n"
            "血清肌酐(mg/dL) = 血清肌酐(μmol/L) / 88.4\n\n"
            "女性肌酐清除率计算：\n"
            "女性肌酐清除率(ml/min) = 男性肌酐清除率(ml/min) × 0.85\n\n"
            "Calvert公式：\n"
            "卡铂剂量(mg) = AUC × [肌酐清除率(ml/min) + 25]"
        )
        ttk.Label(formula_frame, text=formula_text, justify=tk.LEFT).pack(anchor=tk.W)

    def calculate_normal_dose(self):
        """计算普通化疗药剂量"""
        try:
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())
            dose_per_m2 = float(self.dose_entry.get())

            # 计算体表面积（中国通用公式）
            bsa = 0.0061 * height + 0.0124 * weight - 0.0099

            # 计算药物用量
            total_dose_mg = bsa * dose_per_m2
            total_dose_g = total_dose_mg / 1000

            result_text = (
                f"体表面积: {bsa:.2f} m²\n"
                f"拟使用药量: {total_dose_mg:.2f} mg\n"
                f"拟使用药量: {total_dose_g:.2f} g"
            )

            self.normal_result_label.config(text=result_text)

        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")

    def calculate_carboplatin_dose(self):
        """计算卡铂剂量 - 使用修正后的公式"""
        try:
            auc = float(self.auc_entry.get())
            creatinine = float(self.creatinine_entry.get())  # μmol/L
            age = float(self.age_entry.get())
            weight = float(self.weight_entry_carbo.get())
            gender = self.gender_var.get()

            # 计算肌酐清除率（Cockcroft-Gault公式，修改为使用μmol/L单位）
            # 首先将肌酐从μmol/L转换为mg/dL，因为原始公式使用mg/dL
            creatinine_mg_dl = creatinine / 88.4

            # 计算男性肌酐清除率
            male_ccr = ((140 - age) * weight) / (72 * creatinine_mg_dl)

            # 根据性别确定肌酐清除率
            if gender == "女":
                ccr = male_ccr * 0.85
                gender_label = "女性肌酐清除率"
            else:
                ccr = male_ccr
                gender_label = "男性肌酐清除率"

            # 使用Calvert公式计算卡铂剂量
            carboplatin_dose_mg = auc * (ccr + 25)
            carboplatin_dose_g = carboplatin_dose_mg / 1000

            result_text = (
                f"{gender_label}: {ccr:.2f} ml/min\n"
                f"卡铂剂量: {carboplatin_dose_mg:.2f} mg\n"
                f"卡铂剂量: {carboplatin_dose_g:.2f} g"
            )

            self.carboplatin_result_label.config(text=result_text)

        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")
        except ZeroDivisionError:
            messagebox.showerror("计算错误", "血肌酐不能为0")
        except Exception as e:
            messagebox.showerror("计算错误", f"计算出错: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DoseCalculator(root)
    root.mainloop()
