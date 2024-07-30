import FormSlot from "../compoment/FormSlot"
import Logo from "../compoment/Logo";
import MenuList from "../compoment/MenuList";

import { useParams } from "react-router-dom";
import { Layout } from "antd";
const { Sider } = Layout

import "../styles/Home.css";
import "../styles/Sidebar.css";

function NewSlot() {
    const { id } = useParams(); 
    return (<Layout>
        <Sider className="sidebar">
            <Logo />
            <MenuList currnentKey={'create_class'} />
        </Sider>
        < FormSlot route={`class${id}/`}></FormSlot >
    </Layout>
    )
}

export default NewSlot