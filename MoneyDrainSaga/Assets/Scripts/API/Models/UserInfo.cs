namespace API.Models
{
    public class UserInfo
    {
        public int ID;
        public string Username;
        public float Money;

        public override string ToString()
        {
            return $"id: {ID}, username: {Username}, money: {Money}";
        }
    }
}