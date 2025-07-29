import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import { LineChartOutlined, HomeOutlined } from '@ant-design/icons';
import ProductList from './components/ProductList';
import ProductDetail from './components/ProductDetail';
import 'antd/dist/reset.css';

const { Header, Content } = Layout;

const App: React.FC = () => {
    const menuItems = [
        {
            key: '/',
            icon: <HomeOutlined />,
            label: <Link to="/">产品列表</Link>,
        },
    ];

    return (
        <Router>
            <Layout style={{ minHeight: '100vh' }}>
                <Header style={{ display: 'flex', alignItems: 'center' }}>
                    <div style={{ color: 'white', fontSize: '18px', fontWeight: 'bold', marginRight: '24px' }}>
                        <LineChartOutlined /> 量化投资组合管理系统
                    </div>
                    <Menu
                        theme="dark"
                        mode="horizontal"
                        defaultSelectedKeys={['/']}
                        items={menuItems}
                        style={{ flex: 1, minWidth: 0 }}
                    />
                </Header>
                <Content style={{ padding: '0', background: '#f0f2f5' }}>
                    <Routes>
                        <Route path="/" element={<ProductList />} />
                        <Route path="/product/:id" element={<ProductDetail />} />
                    </Routes>
                </Content>
            </Layout>
        </Router>
    );
};

export default App;
