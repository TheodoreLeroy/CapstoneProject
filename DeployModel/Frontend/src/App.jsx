import { BrowserRouter, Route, Routes } from "react-router-dom"
import Login from "./pages/Login"
import Home from "./pages/Home"
import NotFound from "./pages/NotFound"
import Register from "./pages/Register"
import Attendent from "./pages/Attendent"
import Class from "./pages/Class"

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login></Login>} />
        <Route path="/register" element={<Register />} />
        <Route path="/home" element={<Home />} />
        <Route path="/class/:idClass" element={<Class />} />
        <Route path="/class/:idClass/slot/:idSlot" element={<Attendent />} />

        <Route path="/attendent">
          <Route path=":class/:subject" element={<Attendent />} />
        </Route>
        <Route path="*" element={<NotFound></NotFound>}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
