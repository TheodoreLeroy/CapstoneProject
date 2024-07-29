import { Menu } from "antd";
import React, { useState, useEffect } from 'react';
import { AppstoreOutlined, AreaChartOutlined, HomeOutlined, LogoutOutlined, SettingOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

import api from "../api";



const MenuList = (currnentKey) => {

    const [current, setCurrent] = useState(currnentKey.currnentKey);
    const [classNames, setClassNames] = useState([]);

    const navigate = useNavigate()

    useEffect(() => {
        getClass();
    }, [])

    const getClass = () => {
        api.get("addClass/")
            .then((res) => res.data)
            .then((data) => { setClassNames(data); console.log(data); })
            .catch((e) => {
                alert(e)
            })
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
            case 'activity':
                navigate("/attendent");
                break;
            case 'create_class':
                navigate("/NewClass")
                break;
            default:
                navigate(`/${e.key}`)
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
            key: 'progress',
            icon: <AreaChartOutlined />,
            label: 'Class',
            children:
                classNames?.map((className) => (
                    {
                        key: `class/${classNames.indexOf(className)}`,
                        label: className.ClassName + " - " + className.Semester,
                    })),

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
            children: [{
                key: "create_class",
                label: "Add new class",
            },]
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