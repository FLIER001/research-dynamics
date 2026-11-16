# -*- coding: utf-8 -*-
"""给栏目期页加右侧导航目录（桌面右栏、窄屏右侧抽屉）与页脚返回主页链接。
用法：python3 归档/脚本/add_toc.py <html...>  不带参数则处理根目录全部期页。
可重复执行：已注入的页面不会重复注入。
"""
import io, os, re, sys

def find_base():
    """脚本可放在仓库任意子目录：向上找含 index.html 与 style-template.html 的目录。"""
    d = os.path.dirname(os.path.abspath(__file__))
    while d and d != '/':
        if os.path.exists(os.path.join(d, 'index.html')) or os.path.exists(os.path.join(d, 'style-template.html')):
            return d
        d = os.path.dirname(d)
    return os.path.dirname(os.path.abspath(__file__))


BASE = find_base()

CSS = """
/* 右侧目录 */
#tocbtn{position:fixed;right:0;top:42%;z-index:60;display:block;writing-mode:vertical-rl;letter-spacing:2px;
font:14px/1.6 -apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Noto Sans CJK SC","Microsoft YaHei",sans-serif;
padding:9px 4px;background:rgba(255,253,249,.94);color:var(--sub);border:1px solid var(--line);border-right:0;
border-radius:0;cursor:pointer;}
body.toc-open #tocbtn{opacity:0;pointer-events:none;}
#toc{position:fixed;top:0;right:0;bottom:0;width:76%;max-width:300px;background:var(--paper);
border-left:1px solid var(--line);padding:22px 16px 30px;overflow:auto;z-index:70;transform:translateX(101%);
transition:transform .18s ease;font-size:14px;line-height:1.5;}
body.toc-open #toc{transform:none;}
#toc .th{font-size:12px;letter-spacing:2px;color:var(--sub);margin:0 0 12px;}
#toc ol{list-style:none;margin:0;padding:0;}
#toc li{margin:0;}
#toc a{display:block;padding:8px 0;border-bottom:1px solid var(--line);color:var(--ink);text-decoration:none;word-break:normal;}
#toc a:active,#toc a.on{color:var(--accent);}
#toc .close{position:absolute;top:8px;right:10px;background:none;border:0;color:var(--sub);font-size:22px;line-height:1;
padding:6px 8px;cursor:pointer;font-family:inherit;}
@media (min-width:1120px){
 body{display:flex;justify-content:center;align-items:flex-start;gap:40px;}
 main{margin:24px 0 0;flex:0 0 auto;}
 #toc{position:sticky;top:24px;left:auto;right:auto;bottom:auto;transform:none;width:176px;max-width:none;
  max-height:calc(100vh - 48px);border-left:0;background:transparent;padding:30px 0 0;margin:24px 0 0;overflow:auto;}
 #toc .close{display:none;}
 #toc .th{font-size:11px;letter-spacing:3px;margin-bottom:10px;}
 #toc a{font-size:13px;color:var(--sub);border-bottom:0;padding:4px 0;line-height:1.6;}
 #toc a.on{color:var(--accent);font-weight:700;}
 #tocbtn{display:none;}
}
p.home{margin:18px 0 0;text-align:center;font-size:13px;line-height:1.6;}
p.home a{color:var(--sub);letter-spacing:1.5px;opacity:.75;}
p.home a:hover{color:var(--accent);opacity:1;text-decoration:none;}
"""

MARK = """<!--toc:start-->
<button id="tocbtn" type="button" aria-controls="toc" aria-expanded="false">目录</button>
<nav id="toc" aria-label="页内目录"><button class="close" type="button" aria-label="关闭目录">×</button><div class="th">目录</div><ol></ol></nav>
<script>
(function(){
 var nav=document.getElementById('toc'),btn=document.getElementById('tocbtn'),list=nav.querySelector('ol');
 var heads=[].slice.call(document.querySelectorAll('main section > h2'));
 var links=[];
 heads.forEach(function(h,i){
   var id='s'+(i+1);
   var sec=h.parentNode; sec.id=sec.id||id;
   var a=document.createElement('a'); a.href='#'+sec.id; a.textContent=h.textContent.replace(/\\s+/g,' ').trim();
   var li=document.createElement('li'); li.appendChild(a); list.appendChild(li);
   links.push({a:a,sec:sec});
 });
 function close(){document.body.classList.remove('toc-open');btn.setAttribute('aria-expanded','false');}
 btn.addEventListener('click',function(){document.body.classList.add('toc-open');btn.setAttribute('aria-expanded','true');});
 nav.querySelector('.close').addEventListener('click',close);
 list.addEventListener('click',function(e){if(e.target.tagName==='A')close();});
 document.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
 nav.addEventListener('click',function(e){e.stopPropagation();});
 if('IntersectionObserver' in window && links.length){
   var io=new IntersectionObserver(function(es){
     es.forEach(function(en){
       if(!en.isIntersecting)return;
       links.forEach(function(l){l.a.classList.toggle('on',l.sec===en.target);});
     });
   },{rootMargin:'-15% 0px -70% 0px'});
   links.forEach(function(l){io.observe(l.sec);});
 }
})();
</script>
<!--toc:end-->
"""


HOME = """<!--home:start--><p class="home"><a href="index.html">← 返回主页</a></p><!--home:end-->"""


def inject(path):
    s = io.open(path, encoding='utf-8').read()
    if '</style>' not in s or '</body>' not in s:
        return 'bad'
    if '<!--toc:start-->' not in s:
        if '/* 右侧目录 */' not in s:
            s = s.replace('</style>', CSS + '</style>', 1)
        s = s.replace('</body>', MARK + '\n</body>', 1)
        s = s.replace('</main>', HOME + '\n</main>', 1)
        io.open(path, 'w', encoding='utf-8').write(s)
        return 'inject'
    if '<!--toc:start-->' in s:
        s = re.sub(r'\n/\* 右侧目录 \*/.*?(?=\n</style>)', lambda m: CSS.rstrip('\n'), s, count=1, flags=re.S)
        s = re.sub(r'<!--toc:start-->.*?<!--toc:end-->', lambda m: MARK.rstrip('\n'), s, count=1, flags=re.S)
        if '<!--home:start-->' in s:
            s = re.sub(r'<!--home:start-->.*?<!--home:end-->', lambda m: HOME, s, count=1, flags=re.S)
        else:
            s = s.replace('</main>', HOME + '\n</main>', 1)
        io.open(path, 'w', encoding='utf-8').write(s)
        return 'refresh'
    s = s.replace('</style>', CSS + '</style>', 1)
    s = s.replace('</body>', MARK + '\n</body>', 1)
    s = s.replace('</main>', HOME + '\n</main>', 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    return 'ok'


def main():
    args = sys.argv[1:]
    if not args:
        args = [os.path.join(BASE, f) for f in sorted(os.listdir(BASE))
                if re.match(r'(news-brief|research-dynamics|policy-watch|academic-frontier)-\d{8}\.html$', f)]
    for p in args:
        print(inject(p), os.path.basename(p))


if __name__ == '__main__':
    main()
