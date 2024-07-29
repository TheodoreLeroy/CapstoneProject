import FormClass from "../compoment/FormClass"
import "../styles/Home.css";
import "../styles/Sidebar.css";
import Logo from "../compoment/Logo";
import MenuList from "../compoment/MenuList";
import { Layout } from "antd";
const { Sider } = Layout

function NewClass() {
    return (<Layout>
        <Sider className="sidebar">
            <Logo />
            <MenuList currnentKey={'activity'} />
        </Sider>
        < FormClass route="addClass/"></FormClass >
    </Layout>
    )
}

export default NewClass