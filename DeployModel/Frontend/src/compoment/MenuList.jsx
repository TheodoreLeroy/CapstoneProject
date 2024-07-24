import { Menu } from "antd";
import React, { useState } from 'react';
import { AppstoreOutlined, AreaChartOutlined, HomeOutlined, LogoutOutlined, SettingOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";




const items = [
    {
        key: 'home',
        icon: <HomeOutlined />,
        label: 'Home',
    },
    {
        key: 'activity',
        icon: <AppstoreOutlined />,
        label: 'Activity',
    },
    {
        key: 'progress',
        icon: <AreaChartOutlined />,
        label: 'Progress',
    },
    {
        key: 'setting',
        icon: <SettingOutlined />,
        label: 'Setting',
    },
    {
        key: 'logout',
        icon: <LogoutOutlined />,
        label: 'Log out',
    },
];

const MenuList = () => {
    const [current, setCurrent] = useState('home');

    const navigate = useNavigate()

    const onClick = (e) => {
        console.log('click ', e);
        if (e.key === 'logout') {

            localStorage.clear();
            navigate("/login");
        }
        setCurrent(e.key);
    };
    return <Menu onClick={onClick} selectedKeys={[current]} theme="dark" items={items} />;
}

export default MenuList;