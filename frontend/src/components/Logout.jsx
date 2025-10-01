import { useNavigate } from "react-router-dom";

function useLogout() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token"); // remove JWT
    navigate("/"); // redirect to login page
  };

  return logout;
}

export default useLogout;