import "../styles/Home.css";
import "../styles/Sidebar.css";
import Logo from "../compoment/Logo";
import MenuList from "../compoment/MenuList";
import { Layout } from "antd";
const { Header, Sider } = Layout

function Home() {

    return <Layout>
        <Sider className="sidebar">
            <Logo />
            <MenuList currnentKey={'home'} />
        </Sider>
    </Layout>
}

export default Home