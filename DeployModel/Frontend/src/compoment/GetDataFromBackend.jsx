import api from "../api";

function GetDataFromRoute(route) {
    return api.get(route)
        .then((res) => res.data)
        .catch((e) => {
            alert(e);
            return "error";
        });
}

export default GetDataFromRoute;
