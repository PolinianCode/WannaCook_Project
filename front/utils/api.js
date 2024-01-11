import axios from 'axios';
import Cookies from 'js-cookie';


export default function JSONtoURL(json, url_path) {
    const url = `http://localhost:8000/api/${url_path}`
    const data = encodeURIComponent(JSON.stringify(json));
    return `${url}?data=${data}`;
}


const DEFAULT_API_BASE_URL = 'http://localhost:8000/api/';

export const universalApi = async (path = '', method = 'GET', data = null) => {
  const url = DEFAULT_API_BASE_URL + path;

  const config = {
    headers: {
      'X-CSRFToken': getCSRFToken(),
      'Authorization': `Token ${Cookies.get('token')}`,
    },
  };

  const requestConfig = {
    ...config,
    method,
  };

  if (method === 'POST' || method === 'PUT') {
    requestConfig.headers['Content-Type'] = 'application/x-www-form-urlencoded';

    const formData = new URLSearchParams();
    for (const key in data) {
      formData.append(key, data[key]);
    }

    requestConfig.data = formData;
  } else if (data) {

    if (path === 'data/search/') {
        const params = new URLSearchParams();
        for (const key in data) {
          params.append(key, data[key]);
        }
        requestConfig.params = params;
    }else {
        requestConfig[method === 'GET' ? 'params' : 'data'] = data;
    }
   
  }

  try {
    const response = await axios(url, requestConfig);
    return response.data || [];
  } catch (error) {
    throw error.response.data;
  }
};

const getCSRFToken = () => {
  const csrfTokenElement = document.getElementsByName('csrfmiddlewaretoken')[0];
  return csrfTokenElement ? csrfTokenElement.value : null;
};


