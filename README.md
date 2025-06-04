# DoA_Calculate

## 中文说明

### 项目简介

**DoA_Calculate** 用于定量表征碳纳米管（SWNT）阵列的顺直性（Degree of Alignment，DoA）。本项目基于计算机视觉（CV）方法开发了一套程序，用于分析方向比例的提升。具体做法是将单根碳纳米管视为具有特定斜率的线段（图1e），其长度用霍夫空间中对应点被通过的次数表示。通过统计不同方向上的像素数量，实现对碳纳米管阵列取向分布的定量描述。

### 功能介绍

- **Individual_SWNT_Recognition**：利用自训练的机器学习模型对图像进行预处理，比传统的直接二值化（Binarization.ipynb）效果更优。
- **Pixel_Counting_HoughlineP.ipynb**：使用霍夫变换提取线段并计算DoA。
- **Theoretical_distribution.ipynb**：用于验证该方法表征的准确性。
- **FFT_inverse_FFT.ipynb**：传统方法的对比脚本，结果表明本方法优于FFT逆变换方法。

### 使用说明

1. 对原始图像先运行 `Individual_SWNT_Recognition` 进行预处理。
2. 使用 `Pixel_Counting_HoughlineP.ipynb` 进行霍夫变换和像素计数，计算DoA。
3. 用 `Theoretical_distribution.ipynb` 验证结果的准确性。
4. 可用 `FFT_inverse_FFT.ipynb` `Binarization.ipynb`作为传统方法的参考对比。

### 环境依赖

- `pip install -r requirements.txt`

---

## English README

### Overview

**DoA_Calculate** is designed to quantitatively characterize the degree of alignment (DoA) of single-walled carbon nanotube (SWNT) arrays. We developed a set of programs based on computer vision (CV) methods to analyze the improvement in orientation proportion. SWNTs are treated as line segments with specific slopes representing their linear morphology (Figure 1e). The length of each SWNT is quantified by how many times its corresponding point in the Hough space is passed through. The orientation distribution of the SWNT array is thus quantified by counting pixel abundance along directions.

### Features

- **Individual_SWNT_Recognition**: A pretrained machine learning model for preprocessing, which performs significantly better than direct binarization (Binarization.ipynb).
- **Pixel_Counting_HoughlineP.ipynb**: Uses Hough transform to detect line segments and calculate DoA.
- **Theoretical_distribution.ipynb**: Used to validate the accuracy of the characterization method.
- **FFT_inverse_FFT.ipynb**: A traditional FFT-based method used for comparison, showing that our method is superior.

### Usage Instructions

1. Preprocess the raw images with `Individual_SWNT_Recognition`.
2. Calculate DoA with the Hough transform using `Pixel_Counting_HoughlineP.ipynb`.
3. Validate the accuracy using `Theoretical_distribution.ipynb`.
4. Optionally, compare with traditional FFT-based methods using `FFT_inverse_FFT.ipynb` `Binarization.ipynb`.

### 环境依赖

- `pip install -r requirements.txt`
