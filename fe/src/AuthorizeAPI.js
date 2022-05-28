import { useAuth0 } from "@auth0/auth0-react";
//eslint-disable-next-line
import regeneratorRuntime from "regenerator-runtime";

export const authyRequest = async (
  url,
  method = "GET",
  body = null,
  token = null
) => {
  const res = await fetch(url, {
    method: method,
    body: method == "GET" ? undefined : JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

  if (res.status == 200) {
    return await res.json();
  } else {
    return res.status;
  }
};

// export const authorizeAPI = (url, options = {}) => {
//   const { getAccessTokenSilently } = useAuth0();
//   const [state, setState] = useState({
//     error: null,
//     loading: true,
//     data: null,
//   });
//   const [refreshIndex, setRefreshIndex] = useState(0);

//   useEffect(() => {
//     (async () => {
//       try {
//         const { audience, scope, ...fetchOptions } = options;
//         const accessToken = await getAccessTokenSilently({ audience, scope });
//         const res = await fetch(url, {
//           ...fetchOptions,
//           headers: {
//             ...fetchOptions.headers,
//             // Add the Authorization header to the existing headers
//             Authorization: `Bearer ${accessToken}`,
//           },
//         });
//         setState({
//           ...state,
//           data: await res.json(),
//           error: null,
//           loading: false,
//         });
//       } catch (error) {
//         setState({
//           ...state,
//           error,
//           loading: false,
//         });
//       }
//     })();
//   }, [refreshIndex]);

//   return {
//     ...state,
//     refresh: () => setRefreshIndex(refreshIndex + 1),
//   };
// };
