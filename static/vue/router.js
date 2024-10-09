
import about from "./components/about.js";
import home from "./components/home.js";
import UserLogin from "./components/userlogin.js";
import adminhome from "./components/adminhome.js";
import userhome from "./components/userhome.js";
import AdminLogin from "./components/AdminLogin.js";
import AdminRegister from "./components/AdminRegister.js";
import UserRegister from "./components/UserRegister.js";


const routes = [
    {
        path: "/",
        component: home,
        name: "home"
    },
    {
        path: "/about",
        component: about,
        name: "About"
    },
    {
        path: '/userlogin',
        component: UserLogin,
        name: 'UserLogin'
    },
    {
        path: '/adminlogin',
        component: AdminLogin,
        name: 'AdminLogin'
    },
    {
        path: '/user-register',
        component: UserRegister,
        name: 'UserRegister'
    },
    {
        path: '/admin-register',
        component: AdminRegister,
        name: 'AdminRegister'
    },
    {
        path: '/adminhome',
        component: adminhome,
        name: 'Adminhome'
    },
    {
        path: '/userhome',
        component: userhome,
        name: 'Userhome'
    },
    {
        path: "*",
        redirect: "/"
    }
];


const router = new VueRouter({
    routes
});

export default router;