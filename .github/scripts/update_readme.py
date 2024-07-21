import feedparser
import os
from dateutil import parser as date_parser
from urllib.parse import urlsplit, urlunsplit, parse_qs, urlencode

# RSS Feed URLs
RSS_URLS = [
    'https://leixue.com/news/feed',  # 替换为实际的RSS源URL
    'https://leixue.com/ask/feed',
    'https://leixue.com/app/feed',
    # 添加更多RSS源URL
]

# 读取现有的 README.md 文件
def read_readme():
    if os.path.exists('README.md'):
        with open('README.md', 'r') as file:
            return file.read()
    return "## RSS Links\n## End RSS Links\n"  # 如果没有 README.md 文件，则创建一个包含 RSS Links 部分的模板

# 更新 README.md 文件
def update_readme(content):
    with open('README.md', 'w') as file:
        file.write(content)

def fetch_rss_feed(url):
    feed = feedparser.parse(url)
    return feed.entries

def get_pub_date(entry):
    if 'published' in entry:
        return date_parser.parse(entry.published)
    elif 'pubDate' in entry:
        return date_parser.parse(entry.pubDate)
    else:
        return datetime.min  # 如果没有发布日期，返回最小日期

def remove_utm_param(url):
    parts = list(urlsplit(url))
    query = parse_qs(parts[3])
    query.pop('utm_source', None)  # 移除 utm_source 参数
    parts[3] = urlencode(query, doseq=True)
    return urlunsplit(parts)

def main():
    readme_content = read_readme()

    # 获取所有RSS源的内容并合并
    all_entries = []
    for url in RSS_URLS:
        entries = fetch_rss_feed(url)
        all_entries.extend(entries)

    # 按发布时间排序
    all_entries.sort(key=lambda entry: get_pub_date(entry), reverse=True)

    # 生成排序后的链接列表
    rss_links = [f"- [{entry.title}]({remove_utm_param(entry.link)})" for entry in all_entries]
    combined_rss_links = "\n".join(rss_links)

    # 更新 README 内容
    updated_content = readme_content
    rss_section_start = "## RSS Links\n"
    rss_section_end = "\n## End RSS Links"
    start_index = readme_content.find(rss_section_start)
    end_index = readme_content.find(rss_section_end)

    if start_index == -1 or end_index == -1:
        updated_content += f"\n{rss_section_start}{combined_rss_links}{rss_section_end}\n"
    else:
        updated_content = (readme_content[:start_index + len(rss_section_start)] +
                           combined_rss_links +
                           readme_content[end_index:])

    update_readme(updated_content)

if __name__ == "__main__":
    main()
