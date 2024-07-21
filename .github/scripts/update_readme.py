import feedparser
import os

# RSS Feed URL
RSS_URL = 'https://leixue.com/feed'  # 替换为实际的 RSS 源

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

def fetch_rss_feed():
    feed = feedparser.parse(RSS_URL)
    entries = feed.entries
    links = [f"- [{entry.title}]({entry.link})" for entry in entries]
    return "\n".join(links)

def main():
    readme_content = read_readme()
    rss_links = fetch_rss_feed()

    # 更新 README 内容
    updated_content = readme_content
    rss_section_start = "## RSS Links\n"
    rss_section_end = "\n## End RSS Links"
    start_index = readme_content.find(rss_section_start)
    end_index = readme_content.find(rss_section_end)

    if start_index == -1 or end_index == -1:
        updated_content += f"\n{rss_section_start}{rss_links}{rss_section_end}\n"
    else:
        updated_content = (readme_content[:start_index + len(rss_section_start)] +
                           rss_links +
                           readme_content[end_index:])

    update_readme(updated_content)

if __name__ == "__main__":
    main()
