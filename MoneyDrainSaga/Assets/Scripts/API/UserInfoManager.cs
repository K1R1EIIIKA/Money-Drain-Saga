using System.Linq;
using System.Threading.Tasks;
using API.Models;
using Cysharp.Threading.Tasks;
using Newtonsoft.Json.Linq;
using UnityEngine;
using UnityEngine.Networking;

namespace API
{
    public static class UserInfoManager
    {
        private const string UserInfoUrl = "http://127.0.0.1:8001/user";
        public static async UniTask<UserInfo> GetUserInfoAsync()
        {
            using (UnityWebRequest www = UnityWebRequest.Get(UserInfoUrl))
            {
                string cookie = PlayerPrefs.GetString("cookie");
                var jwt = cookie.Split(';') // Разделяем по ";"
                    .FirstOrDefault(x => x.Trim().StartsWith("jwt="));
                jwt = jwt.Replace("jwt=", "");

                Debug.Log(jwt);

                www.SetRequestHeader("jwt", jwt);

                var asyncOperation = www.SendWebRequest();
                while (!asyncOperation.isDone)
                {
                    await Task.Yield();
                }

                if (www.result == UnityWebRequest.Result.ConnectionError ||
                    www.result == UnityWebRequest.Result.ProtocolError)
                {
                    Debug.Log(www.error);
                    // IsAuthorized = false;
                    return null;
                }

                var jsonResponse = www.downloadHandler.text;
                var userInfoJson = JObject.Parse(jsonResponse);

                return new UserInfo
                {
                    ID = userInfoJson.Value<int>("id"),
                    Username = userInfoJson.Value<string>("username"),
                    Money = userInfoJson.Value<float>("money")
                };
            }
        }
    }
}