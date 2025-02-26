import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import unicodedata

# 配置信息 - 替换为你的应用凭证
SPOTIPY_CLIENT_ID = ' '
SPOTIPY_CLIENT_SECRET = ' '
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# 请求权限范围
SCOPE = 'user-top-read user-library-read'

# 计算字符宽度（考虑中文字符）
def get_char_width(s):
    return sum(2 if unicodedata.east_asian_width(c) in ('F', 'W') else 1 for c in s)

# 颜色设置，根据流行度调整
def get_color(popularity):
    if popularity > 90:
        return '\033[91m'  # 红色
    elif popularity > 50:
        return '\033[93m'  # 黄色
    else:
        return '\033[92m'  # 绿色

# 获取Spotify数据
def get_spotify_data(time_range):
    # 初始化OAuth管理器
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE
    ))

    # 获取最常听的歌曲
    print("Loading...", end='', flush=True)
    print("\r", end='', flush=True)
    top_tracks = sp.current_user_top_tracks(time_range=time_range, limit=10)
    print(' '*20)
    print(f"\n=== {range2output[time_range]}最常听的歌曲 ===")
    for idx, item in enumerate(top_tracks['items']):
        track_name = item['name']
        artist_name = item['artists'][0]['name']
        popularity = item['popularity']
        color = get_color(popularity)
        
        # 计算歌曲名和艺术家的实际字符宽度（考虑中文）
        track_width = get_char_width(track_name)
        artist_width = get_char_width(artist_name)

        # 动态计算适当的对齐宽度
        track_name_display = f"{track_name:<40}" if track_width <= 40 else f"{track_name[:37]}..."
        artist_name_display = f"{artist_name:<20}" if artist_width <= 30 else f"{artist_name[:17]}..."
        
        # 打印歌曲信息，按格式对齐
        print(f"{idx+1:2}. {color}{track_name_display} - {artist_name_display} | Popularity: {popularity}%\033[0m")

    # 获取最常听的艺术家
    print(f"\n=== {range2output[time_range]}最常听的艺术家 ===")
    top_artists = sp.current_user_top_artists(time_range=time_range, limit=10)
    for idx, artist in enumerate(top_artists['items']):
        artist_name = artist['name']
        popularity = artist['popularity']
        color = get_color(popularity)
        
        # 计算艺术家的实际字符宽度（考虑中文）
        artist_width = get_char_width(artist_name)

        # 动态计算适当的对齐宽度
        artist_name_display = f"{artist_name:<40}" if artist_width <= 40 else f"{artist_name[:37]}..."

        # 打印艺术家信息，按格式对齐
        print(f"{idx+1:2}. {color}{artist_name_display} | Popularity: {popularity}%\033[0m")


if __name__ == "__main__":
    input2range = {'s': 'short_term', 'm': 'medium_term', 'l': 'long_term'}
    range2output = {'short_term': '4周内', 'medium_term': '6个月内', 'long_term': '所有时间'}

    # 从命令行参数获取时间范围
    if len(sys.argv) < 2:
        print("请提供时间范围: s, m 或 l")
        sys.exit(1)

    input = sys.argv[1]
    # 确保时间范围有效
    if input not in ['s', 'm', 'l']:
        print("无效的时间范围! 请选择 s, m 或 l(4周内， 6个月内， 所有时间)")
        sys.exit(1)
    time_range = input2range[input]
    
    get_spotify_data(time_range)
