import "../styles/Home.css";
import "../styles/Sidebar.css";
import Logo from "../compoment/Logo";
import MenuList from "../compoment/MenuList";
import Slot from "../compoment/Slot";
import { Layout } from "antd";
import { useParams } from "react-router-dom";
const { Sider } = Layout

function Attendent() {
    let params = useParams();
    console.log(params)
    return <Layout>
        <Sider className="sidebar">
            <Logo />
            <MenuList currnentKey={'activity'} />
        </Sider>
        <Slot params={params}></Slot>
    </Layout>
}

export default Attendent