using System;
using System.Collections;
using System.Linq;
using System.Threading.Tasks;
using API.Models;
using Cysharp.Threading.Tasks;
using Newtonsoft.Json.Linq;
using UnityEngine;
using UnityEngine.Networking;

namespace API
{
    public class AuthManager : MonoBehaviour
    {
        public UserInfo UserInfoData { get; set; }

        private const string LoginUrl = "http://127.0.0.1:8001/login";
        private const string LogoutUrl = "http://127.0.0.1:8001/logout";
        private LoginResponse _loginResponse;

        public static AuthManager Instance { get; private set; }

        private void Awake()
        {
            _loginResponse = new LoginResponse();

            if (Instance == null)
                Instance = this;
            else
                Destroy(gameObject);
        }

        private async void Update()
        {
            if (Input.GetKeyDown(KeyCode.Space))
            {
                await Login("k1r1eiiika", "12345");
            }

            if (Input.GetKeyDown(KeyCode.Alpha1))
            {
                var info = await UserInfoManager.GetUserInfoAsync();
                Debug.Log(info);
            }
        }

        private IEnumerator CheckInternetConnection()
        {
            using (UnityWebRequest www = UnityWebRequest.Get("https://www.google.com/"))
            {
                yield return www.SendWebRequest();

                if (www.result == UnityWebRequest.Result.ConnectionError ||
                    www.result == UnityWebRequest.Result.ProtocolError)
                {
                    Debug.Log("No Internet Connection");
                }
                else
                {
                    Debug.Log("Internet Connection Available");
                }
            }
        }

        public async UniTask<bool> Login(string username, string password)
        {
            WWWForm form = new WWWForm();
            form.AddField("username", username);
            form.AddField("password", password);

            using (UnityWebRequest www = UnityWebRequest.Post(LoginUrl, form))
            {
                var asyncOperation = www.SendWebRequest();

                while (!asyncOperation.isDone)
                {
                    await Task.Yield();
                }

                if (www.result == UnityWebRequest.Result.Success)
                {
                    var jsonResponse = www.downloadHandler.text;
                    var loginResponseJson = JObject.Parse(jsonResponse);
                    string jwt = loginResponseJson.Value<string>("jwt");
                    string refreshJwt = loginResponseJson.Value<string>("refresh_jwt");

                    if (!string.IsNullOrEmpty(jwt) && !string.IsNullOrEmpty(refreshJwt))
                    {
                        // Сохранение JWT токенов и куки
                        PlayerPrefs.SetString("jwt", jwt);
                        PlayerPrefs.SetString("refreshJwt", refreshJwt);
                        PlayerPrefs.Save();

                        // UserInfoManager.IsAuthorized = true;

                        foreach (var header in www.GetResponseHeaders())
                        {
                            if (header.Key.ToLower() == "set-cookie")
                            {
                                PlayerPrefs.SetString("cookie", header.Value);
                            }
                        }

                        Debug.Log("Successfully logged in. JWT: " + jwt + " Refresh JWT: " + refreshJwt);
                        return true;
                    }

                    Debug.LogError("Invalid login response");
                    return false;
                }

                Debug.LogError("Login failed: " + www.error);
                return false;
            }
        }


        public async Task<bool> Logout()
        {
            using (UnityWebRequest www = UnityWebRequest.PostWwwForm(LogoutUrl, ""))
            {
                // www.SetRequestHeader("Authorization", "Bearer " + loginResponse.jwt);
                var asyncOperation = www.SendWebRequest();
                while (!asyncOperation.isDone)
                {
                    await Task.Yield();
                }

                if (www.result == UnityWebRequest.Result.Success)
                {
                    Debug.Log("Logout successful");
                    PlayerPrefs.DeleteKey("jwt");
                    PlayerPrefs.DeleteKey("refreshJwt");
                    PlayerPrefs.DeleteKey("cookie");
                    PlayerPrefs.Save();
                    // UserInfoManager.IsAuthorized = false;
                    return true;
                }

                Debug.LogError("Logout failed" + www.error);
                return false;
            }
        }
    }
}