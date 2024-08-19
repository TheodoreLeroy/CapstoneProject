import { Menu } from "antd";
import React, { useState, useEffect } from 'react';
import { AreaChartOutlined, HomeOutlined, LogoutOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

import GetDataFromRoute from "./GetDataFromBackend";


const MenuList = (currnentKey) => {
    const [current, setCurrent] = useState(currnentKey.currnentKey);
    const [classNames, setClassNames] = useState([]);

    const navigate = useNavigate()

    useEffect(() => {
        getClass();
    }, [])

    const getClass = async () => {
        const classData = await GetDataFromRoute("classes/detail");
        setClassNames(classData);
    }
    
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
            default:
                navigate(`/${e.key}`)
                window.location.reload();
                break;
        }

    };
    const items = [
        {
            key: 'home',
            icon: <HomeOutlined />,
            label: 'Home',
        },
        {
            key: 'class',
            icon: <AreaChartOutlined />,
            label: 'Class',
            children:
                classNames?.map((className) => (
                    {
                        key: `classes/${className.id}`,
                        label: className.class_name + " - " + className.semester,
                    })),

        },
        {
            key: 'logout',
            icon: <LogoutOutlined />,
            label: 'Log out',
        },
    ];
    return <Menu mode="inline" onClick={onClick} selectedKeys={[current]} theme="dark" items={items} />;
}

export default MenuList;