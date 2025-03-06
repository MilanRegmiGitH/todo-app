const BASE_URL = "http://localhost:8000";


export const API_PATH = {
    AUTH:{
        LOGIN: `${BASE_URL}/token`,
        SIGN_UP:`${BASE_URL}/register`
    },
    POST:{
        CREATE_TASK: `${BASE_URL}/tasks`
    },
    GET:{
        GET_TASKS: `${BASE_URL}/get_tasks`
    },
    PUT:{

    },
    DELETE:{
        DELETE_TASK:`${BASE_URL}/tasks`
    },
    PATCH:{
        UPDATE_TASK:`${BASE_URL}/tasks`
    }
}