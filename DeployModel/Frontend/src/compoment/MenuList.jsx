import { Menu } from "antd";
import React, { useState, useEffect } from 'react';
import { AppstoreOutlined, AreaChartOutlined, HomeOutlined, LogoutOutlined, SettingOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

const items = [
    {
        key: 'home',
        icon: <HomeOutlined />,
        label: 'Home',
    },    
    {
        key: 'progress',
        icon: <AreaChartOutlined />,
        label: 'Class',
        children: [
            {
                key: 'attendent/class',
                label: '1',
                children: [
                    {
                        key: `attendent/5/Math`,
                        label: 'Math',
                    },
                    {
                        key: 'attendent/5/English',
                        label: 'English',
                    },
                    {
                        key: 'attendent/5/Physic',
                        label: 'Physic',
                    },
                ],
            },
            {
                key: '24',
                label: '2',
                children: [
                    {
                        key: '241',
                        label: 'Option 1',
                    },
                    {
                        key: '242',
                        label: 'Option 2',
                    },
                    {
                        key: '243',
                        label: 'Option 3',
                    },
                ],
            },
        ],
    },
    {
        key: 'activity',
        icon: <AppstoreOutlined />,
        label: 'Activity',
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

const MenuList = (currnentKey) => {

    const [current, setCurrent] = useState(currnentKey.currnentKey);

    const navigate = useNavigate()

    const onClick = (e) => {
        setCurrent(currnentKey.currnentKey)
        console.log('click e.key: ', e.key);
        console.log('click currnentKey: ', current);
        if (e.key === 'logout') {

        }
        switch (e.key) {
            case 'home':
                navigate("/home");
                break;
            case 'logout':
                localStorage.clear();
                navigate("/login");
                break;
            case 'activity':
                navigate("/attendent");
                break;
            default:
                navigate(`/${e.key}`)
                break;
        }

    };
    return <Menu mode="inline" onClick={onClick} selectedKeys={[current]} theme="dark" items={items} />;
}

export default MenuList;