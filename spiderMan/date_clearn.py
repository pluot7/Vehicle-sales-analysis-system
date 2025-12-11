import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import re
import warnings

warnings.filterwarnings('ignore')


class CarDataCleaner:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cleaned_df = None
        self.scaler = StandardScaler()
        self.models = {}

    def load_data(self):
        """加载CSV数据"""
        try:
            self.df = pd.read_csv(self.file_path)
            print(f"数据加载成功，共 {len(self.df)} 行，{len(self.df.columns)} 列")
            return True
        except Exception as e:
            print(f"数据加载失败: {e}")
            return False

    def explore_data(self):
        """数据探索分析"""
        print("=" * 50)
        print("数据探索分析")
        print("=" * 50)

        # 基本信息
        print(f"数据形状: {self.df.shape}")
        print("\n列名:")
        print(self.df.columns.tolist())

        print("\n前5行数据:")
        print(self.df.head())

        print("\n数据类型:")
        print(self.df.dtypes)

        print("\n缺失值统计:")
        missing_data = self.df.isnull().sum()
        print(missing_data[missing_data > 0])

        print("\n数值列描述性统计:")
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(self.df[numeric_cols].describe())

        return self.df

    def extract_price_range(self, price_str):
        """从价格字符串中提取价格范围"""
        try:
            if isinstance(price_str, str) and price_str.startswith('['):
                # 移除方括号并分割
                prices = price_str.strip('[]').split(',')
                min_price = float(prices[0].strip())
                max_price = float(prices[1].strip())
                avg_price = (min_price + max_price) / 2
                return min_price, max_price, avg_price
            else:
                return np.nan, np.nan, np.nan
        except:
            return np.nan, np.nan, np.nan

    def preprocess_price(self):
        """预处理价格数据"""
        print("\n预处理价格数据...")

        # 提取价格信息
        price_data = self.df['price'].apply(self.extract_price_range)
        self.df['min_price'] = price_data.apply(lambda x: x[0] if not pd.isna(x[0]) else np.nan)
        self.df['max_price'] = price_data.apply(lambda x: x[1] if not pd.isna(x[1]) else np.nan)
        self.df['avg_price'] = price_data.apply(lambda x: x[2] if not pd.isna(x[2]) else np.nan)

        print(f"价格数据处理完成，平均价格范围: {self.df['avg_price'].min():.2f} - {self.df['avg_price'].max():.2f}")

    def extract_warranty_info(self, warranty_str):
        """从保修信息中提取年限和里程"""
        try:
            if isinstance(warranty_str, str):
                # 使用正则表达式提取数字
                years_match = re.search(r'(\d+)\s*年', warranty_str)
                mileage_match = re.search(r'(\d+)\s*万公里', warranty_str)

                years = float(years_match.group(1)) if years_match else np.nan
                mileage = float(mileage_match.group(1)) * 10000 if mileage_match else np.nan

                return years, mileage
            return np.nan, np.nan
        except:
            return np.nan, np.nan

    def preprocess_warranty(self):
        """预处理保修信息"""
        print("\n预处理保修信息...")

        warranty_data = self.df['insure'].apply(self.extract_warranty_info)
        self.df['warranty_years'] = warranty_data.apply(lambda x: x[0] if not pd.isna(x[0]) else np.nan)
        self.df['warranty_mileage'] = warranty_data.apply(lambda x: x[1] if not pd.isna(x[1]) else np.nan)

        print(f"保修信息处理完成")

    def detect_outliers_neural(self, features, contamination=0.05):
        """使用神经网络检测异常值"""
        print("\n使用神经网络检测异常值...")

        # 使用 Isolation Forest（基于神经网络思想）
        iso_forest = IsolationForest(contamination=contamination, random_state=42)

        # 处理缺失值
        imputer = SimpleImputer(strategy='median')
        features_imputed = imputer.fit_transform(features)

        # 标准化
        features_scaled = self.scaler.fit_transform(features_imputed)

        # 检测异常值
        outliers = iso_forest.fit_predict(features_scaled)

        outlier_indices = np.where(outliers == -1)[0]
        print(f"检测到 {len(outlier_indices)} 个异常值")

        return outlier_indices

    def handle_missing_values_neural(self):
        """使用神经网络方法处理缺失值"""
        print("\n使用神经网络方法处理缺失值...")

        # 选择数值特征进行缺失值预测
        numeric_features = ['saleVolume', 'rank', 'min_price', 'max_price', 'avg_price']

        for feature in numeric_features:
            if self.df[feature].isnull().sum() > 0:
                print(f"处理 {feature} 的缺失值...")

                # 准备训练数据
                known_data = self.df[self.df[feature].notnull()]
                unknown_data = self.df[self.df[feature].isnull()]

                if len(known_data) > 10 and len(unknown_data) > 0:
                    # 选择相关特征
                    other_features = [f for f in numeric_features if f != feature and self.df[f].notnull().all()]

                    if len(other_features) >= 2:
                        X_train = known_data[other_features]
                        y_train = known_data[feature]
                        X_pred = unknown_data[other_features]

                        # 使用神经网络回归预测缺失值
                        nn_model = MLPRegressor(hidden_layer_sizes=(50, 25), random_state=42, max_iter=1000)
                        nn_model.fit(X_train, y_train)

                        predictions = nn_model.predict(X_pred)
                        self.df.loc[self.df[feature].isnull(), feature] = predictions

                        print(f"  使用神经网络填充了 {len(predictions)} 个缺失值")

        # 对于分类变量，使用众数填充
        categorical_features = ['energyType', 'carModel']
        for feature in categorical_features:
            if self.df[feature].isnull().sum() > 0:
                mode_value = self.df[feature].mode()[0]
                self.df[feature].fillna(mode_value, inplace=True)
                print(f"  使用众数填充 {feature} 的缺失值: {mode_value}")

    def validate_and_correct_data(self):
        """验证和修正数据逻辑"""
        print("\n验证和修正数据逻辑...")

        # 1. 验证价格范围合理性
        price_invalid = self.df[self.df['min_price'] > self.df['max_price']]
        if len(price_invalid) > 0:
            print(f"修正 {len(price_invalid)} 条价格范围不合理的数据")
            # 交换最小最大价格
            mask = self.df['min_price'] > self.df['max_price']
            temp = self.df.loc[mask, 'min_price'].copy()
            self.df.loc[mask, 'min_price'] = self.df.loc[mask, 'max_price']
            self.df.loc[mask, 'max_price'] = temp
            self.df.loc[mask, 'avg_price'] = (self.df.loc[mask, 'min_price'] + self.df.loc[mask, 'max_price']) / 2

        # 2. 验证销量非负
        negative_sales = self.df[self.df['saleVolume'] < 0]
        if len(negative_sales) > 0:
            print(f"修正 {len(negative_sales)} 条负销量数据")
            self.df.loc[self.df['saleVolume'] < 0, 'saleVolume'] = 0

        # 3. 验证排名合理性
        invalid_rank = self.df[self.df['rank'] <= 0]
        if len(invalid_rank) > 0:
            print(f"修正 {len(invalid_rank)} 条无效排名数据")
            self.df.loc[self.df['rank'] <= 0, 'rank'] = self.df['rank'].max() + 1

    def create_derived_features(self):
        """创建衍生特征"""
        print("\n创建衍生特征...")

        # 价格区间分类
        def price_category(avg_price):
            if avg_price < 10:
                return '经济型'
            elif avg_price < 20:
                return '中端'
            elif avg_price < 30:
                return '高端'
            else:
                return '豪华型'

        self.df['price_category'] = self.df['avg_price'].apply(price_category)

        # 销量等级
        def sales_level(sales):
            if sales < 10000:
                return '低销量'
            elif sales < 50000:
                return '中等销量'
            else:
                return '高销量'

        self.df['sales_level'] = self.df['saleVolume'].apply(sales_level)

        # 品牌热度（基于该品牌车型数量）
        brand_popularity = self.df['brand'].value_counts()
        self.df['brand_popularity'] = self.df['brand'].map(brand_popularity)

        print("衍生特征创建完成")

    def build_validation_model(self):
        """构建数据验证神经网络模型"""
        print("\n构建数据验证神经网络模型...")

        # 准备特征
        features = ['saleVolume', 'min_price', 'max_price', 'avg_price', 'rank']

        # 检查并处理缺失值
        data_for_model = self.df[features].copy()
        data_for_model = data_for_model.fillna(data_for_model.median())

        # 标准化
        X_scaled = self.scaler.fit_transform(data_for_model)

        # 构建自编码器用于异常检测
        input_dim = X_scaled.shape[1]

        # 简单的自编码器
        encoder = keras.Sequential([
            layers.Dense(32, activation='relu', input_shape=(input_dim,)),
            layers.Dense(16, activation='relu'),
            layers.Dense(8, activation='relu')
        ])

        decoder = keras.Sequential([
            layers.Dense(16, activation='relu', input_shape=(8,)),
            layers.Dense(32, activation='relu'),
            layers.Dense(input_dim, activation='linear')
        ])

        autoencoder = keras.Sequential([encoder, decoder])
        autoencoder.compile(optimizer='adam', loss='mse')

        # 训练自编码器
        history = autoencoder.fit(
            X_scaled, X_scaled,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )

        self.models['autoencoder'] = autoencoder
        self.models['scaler'] = self.scaler

        print("数据验证模型训练完成")

        return history

    def predict_anomalies(self, threshold_ratio=1.5):
        """使用训练好的模型预测异常值"""
        if 'autoencoder' not in self.models:
            print("请先训练模型")
            return None

        features = ['saleVolume', 'min_price', 'max_price', 'avg_price', 'rank']
        data_for_model = self.df[features].copy()
        data_for_model = data_for_model.fillna(data_for_model.median())

        X_scaled = self.models['scaler'].transform(data_for_model)

        # 获取重构值
        reconstructed = self.models['autoencoder'].predict(X_scaled)

        # 计算重构误差
        mse = np.mean(np.power(X_scaled - reconstructed, 2), axis=1)

        # 设置阈值
        threshold = np.percentile(mse, 75) * threshold_ratio

        # 标记异常值
        anomalies = mse > threshold
        anomaly_indices = np.where(anomalies)[0]

        print(f"神经网络检测到 {len(anomaly_indices)} 个潜在异常数据点")

        # 添加异常分数到数据框
        self.df['anomaly_score'] = mse
        self.df['is_anomaly'] = anomalies

        return anomaly_indices

    def generate_cleaning_report(self):
        """生成数据清洗报告"""
        print("\n" + "=" * 50)
        print("数据清洗报告")
        print("=" * 50)

        report = {
            'original_rows': len(self.df),
            'cleaned_rows': len(self.df),
            'numeric_columns': len(self.df.select_dtypes(include=[np.number]).columns),
            'categorical_columns': len(self.df.select_dtypes(include=['object']).columns),
            'missing_values_remaining': self.df.isnull().sum().sum(),
            'potential_anomalies': self.df['is_anomaly'].sum() if 'is_anomaly' in self.df.columns else 0
        }

        for key, value in report.items():
            print(f"{key}: {value}")

        # 显示前10个潜在异常
        if 'is_anomaly' in self.df.columns and self.df['is_anomaly'].sum() > 0:
            print("\n前10个潜在异常数据:")
            anomalies = self.df[self.df['is_anomaly'] == True]
            print(anomalies[['brand', 'carName', 'saleVolume', 'avg_price', 'anomaly_score']].head(10))

        return report

    def save_cleaned_data(self, output_path='cleaned_car_data.csv'):
        """保存清洗后的数据"""
        self.cleaned_df = self.df.copy()
        self.cleaned_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"\n清洗后的数据已保存至: {output_path}")

        return self.cleaned_df

    def visualize_cleaning_results(self):
        """可视化清洗结果"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        # 1. 价格分布
        axes[0, 0].hist(self.df['avg_price'].dropna(), bins=50, alpha=0.7, color='skyblue')
        axes[0, 0].set_title('平均价格分布')
        axes[0, 0].set_xlabel('平均价格 (万元)')
        axes[0, 0].set_ylabel('频数')

        # 2. 销量分布
        axes[0, 1].hist(self.df['saleVolume'], bins=50, alpha=0.7, color='lightgreen')
        axes[0, 1].set_title('销量分布')
        axes[0, 1].set_xlabel('销量')
        axes[0, 1].set_ylabel('频数')

        # 3. 能源类型分布
        energy_counts = self.df['energyType'].value_counts()
        axes[1, 0].pie(energy_counts.values, labels=energy_counts.index, autopct='%1.1f%%')
        axes[1, 0].set_title('能源类型分布')

        # 4. 异常值检测结果
        if 'is_anomaly' in self.df.columns:
            anomaly_counts = self.df['is_anomaly'].value_counts()
            axes[1, 1].bar(['正常', '异常'], anomaly_counts.values, color=['lightblue', 'lightcoral'])
            axes[1, 1].set_title('异常值检测结果')
            axes[1, 1].set_ylabel('数量')

        plt.tight_layout()
        plt.savefig('data_cleaning_visualization.png', dpi=300, bbox_inches='tight')
        plt.show()

    def run_complete_cleaning(self):
        """运行完整的数据清洗流程"""
        print("开始汽车数据清洗流程...")

        # 1. 加载数据
        if not self.load_data():
            return None

        # 2. 数据探索
        self.explore_data()

        # 3. 预处理价格数据
        self.preprocess_price()

        # 4. 预处理保修信息
        self.preprocess_warranty()

        # 5. 处理缺失值
        self.handle_missing_values_neural()

        # 6. 数据验证和修正
        self.validate_and_correct_data()

        # 7. 创建衍生特征
        self.create_derived_features()

        # 8. 构建验证模型
        self.build_validation_model()

        # 9. 检测异常值
        self.predict_anomalies()

        # 10. 生成报告
        report = self.generate_cleaning_report()

        # 11. 可视化结果
        self.visualize_cleaning_results()

        # 12. 保存清洗后的数据
        cleaned_data = self.save_cleaned_data()

        print("\n数据清洗流程完成!")
        return cleaned_data


# 使用示例
if __name__ == "__main__":
    # 初始化数据清洗器
    cleaner = CarDataCleaner('temp.csv')

    # 运行完整清洗流程
    cleaned_data = cleaner.run_complete_cleaning()

    if cleaned_data is not None:
        print(f"\n清洗后的数据形状: {cleaned_data.shape}")
        print(
            f"新增列: {[col for col in cleaned_data.columns if col not in ['brand', 'carName', 'carImg', 'saleVolume', 'price', 'manufacturer', 'rank', 'carModel', 'energyType', 'marketTime', 'insure']]}")