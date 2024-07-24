import { useState, useEffect } from "react";
import api from "../api";
import "../styles/Home.css";
import "../styles/Sidebar.css";
import Logo from "../compoment/Logo";
import MenuList from "../compoment/MenuList";
import Slot from "../compoment/Slot";
import { useNavigate } from "react-router-dom";
import { Layout } from "antd";
const { Header, Sider } = Layout

function Home() {

    return <Layout>
        <Sider className="sidebar">
            <Logo />
            <MenuList />
        </Sider>
        <Slot></Slot>
    </Layout>
}

export default Home