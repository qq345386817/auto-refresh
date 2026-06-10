const LOCALE_ALIASES = {
  "en": "en-US",
  "en-us": "en-US",
  "en_us": "en-US",
  "zh-hans": "zh-Hans",
  "zh_hans": "zh-Hans",
  "zh-cn": "zh-Hans",
  "zh-hant": "zh-Hant",
  "zh_hant": "zh-Hant",
  "zh-tw": "zh-Hant",
  "de": "de-DE",
  "de-de": "de-DE",
  "fr": "fr-FR",
  "fr-fr": "fr-FR",
  "es": "es-ES",
  "es-es": "es-ES",
  "pt": "pt-PT",
  "pt-pt": "pt-PT",
  "ar": "ar-SA",
  "ar-sa": "ar-SA",
  "ja": "ja",
  "ko": "ko"
};

const FALLBACK = "en-US";

const I18N = {
  "en-US": {
    lang: "en-US",
    dir: "ltr",
    title: "Northstar News",
    mark: "N",
    sectionsLabel: "Sections",
    sections: ["Top", "Launches", "Design", "AI", "Markets", "Tools"],
    kicker: "Live coverage",
    latest: "Latest stories",
    more: "More",
    done: "All caught up",
    toast: "More stories loaded",
    comments: "comments",
    pages: [
      {
        count: "Page 1 of 30",
        live: "Updated just now",
        headline: "Independent builders are shipping faster on mobile.",
        summary: "A rolling digest of launches, product news, and industry updates from the past hour.",
        stories: [
          ["A compact editor for quick launch notes", "18 points", "4 comments"],
          ["How a small team handles a midnight release", "31 points", "12 comments"],
          ["A new dashboard tracks waitlists in real time", "27 points", "8 comments"],
          ["Design details that made a tiny app feel faster", "22 points", "6 comments"],
          ["Developers test a leaner checkout flow", "19 points", "3 comments"],
          ["A field report from a product demo day", "15 points", "2 comments"]
        ]
      },
      {
        count: "Page 2 of 30",
        live: "Updated 5 sec ago",
        headline: "New launches are moving from waitlist to public release.",
        summary: "Fresh updates are now available from the next page of the live feed.",
        stories: [
          ["A chip startup announces its first developer kit", "86 points", "24 comments"],
          ["A calendar app adds shared booking pages", "74 points", "19 comments"],
          ["A startup posts new pricing experiments", "61 points", "14 comments"],
          ["Open-source database project adds vector search", "58 points", "11 comments"],
          ["Designers share a cleaner mobile settings panel", "43 points", "9 comments"],
          ["Small apps are winning with clearer onboarding", "39 points", "7 comments"]
        ]
      },
      {
        count: "Page 3 of 30",
        live: "Updated 10 sec ago",
        headline: "The final batch adds follow-up analysis and reader notes.",
        summary: "The feed has reached the latest set of stories for this session.",
        stories: [
          ["Reader notes from today's launch coverage", "97 points", "31 comments"],
          ["What changed after the latest product release", "88 points", "22 comments"],
          ["Teams compare notes from a live demo day", "76 points", "17 comments"],
          ["A practical guide to public status pages", "64 points", "13 comments"],
          ["Fresh API examples arrive in developer docs", "52 points", "10 comments"],
          ["Weekend projects that shipped before noon", "49 points", "8 comments"]
        ]
      }
    ]
  },
  "zh-Hans": {
    lang: "zh-CN",
    dir: "ltr",
    title: "今日快讯",
    mark: "今",
    sectionsLabel: "栏目",
    sections: ["热门", "发布", "设计", "AI", "市场", "工具"],
    kicker: "实时报道",
    latest: "最新动态",
    more: "更多",
    done: "已是最新",
    toast: "已加载更多内容",
    comments: "评论",
    pages: [
      {
        count: "第 1 / 30 页",
        live: "刚刚更新",
        headline: "独立开发者正在更快地发布移动产品。",
        summary: "过去一小时的产品发布、工具更新和行业动态摘要。",
        stories: [
          ["一款轻量编辑器简化发布记录", "18 分", "4 条评论"],
          ["小团队如何处理午夜版本发布", "31 分", "12 条评论"],
          ["新的看板实时追踪候补名单", "27 分", "8 条评论"],
          ["让小应用更快的设计细节", "22 分", "6 条评论"],
          ["开发者测试更精简的结账流程", "19 分", "3 条评论"],
          ["一次产品演示日的现场记录", "15 分", "2 条评论"]
        ]
      },
      {
        count: "第 2 / 30 页",
        live: "5 秒前更新",
        headline: "新的产品发布正在从等待名单走向公开。",
        summary: "实时信息流的下一页已经出现新的内容。",
        stories: [
          ["芯片创业公司发布首款开发套件", "86 分", "24 条评论"],
          ["日历应用加入共享预约页面", "74 分", "19 条评论"],
          ["一家创业公司公布新的定价实验", "61 分", "14 条评论"],
          ["开源数据库项目加入向量搜索", "58 分", "11 条评论"],
          ["设计师分享更清爽的移动设置面板", "43 分", "9 条评论"],
          ["小型应用凭借清晰引导赢得用户", "39 分", "7 条评论"]
        ]
      },
      {
        count: "第 3 / 30 页",
        live: "10 秒前更新",
        headline: "最后一批内容加入后续分析和读者笔记。",
        summary: "本次会话已经到达最新一组资讯。",
        stories: [
          ["今日发布报道的读者笔记", "97 分", "31 条评论"],
          ["最新产品发布之后发生了什么", "88 分", "22 条评论"],
          ["团队交流现场演示日经验", "76 分", "17 条评论"],
          ["公开状态页的实用指南", "64 分", "13 条评论"],
          ["开发者文档加入新的 API 示例", "52 分", "10 条评论"],
          ["午前完成发布的周末项目", "49 分", "8 条评论"]
        ]
      }
    ]
  },
  "zh-Hant": {
    lang: "zh-Hant",
    dir: "ltr",
    title: "今日快訊",
    mark: "今",
    sectionsLabel: "欄目",
    sections: ["熱門", "發布", "設計", "AI", "市場", "工具"],
    kicker: "即時報導",
    latest: "最新動態",
    more: "更多",
    done: "已是最新",
    toast: "已載入更多內容",
    comments: "留言",
    pages: []
  },
  "ja": {
    lang: "ja",
    dir: "ltr",
    title: "Northstar News",
    mark: "N",
    sectionsLabel: "セクション",
    sections: ["トップ", "ローンチ", "デザイン", "AI", "市場", "ツール"],
    kicker: "ライブ更新",
    latest: "最新ストーリー",
    more: "さらに表示",
    done: "最新です",
    toast: "さらに読み込みました",
    points: "ポイント",
    comments: "件のコメント",
    pages: []
  },
  "ko": {
    lang: "ko",
    dir: "ltr",
    title: "Northstar News",
    mark: "N",
    sectionsLabel: "섹션",
    sections: ["인기", "출시", "디자인", "AI", "시장", "도구"],
    kicker: "실시간 소식",
    latest: "최신 소식",
    more: "더 보기",
    done: "모두 확인함",
    toast: "소식을 더 불러왔습니다",
    points: "점",
    comments: "댓글",
    pages: []
  },
  "de-DE": {
    lang: "de-DE",
    dir: "ltr",
    title: "Northstar News",
    mark: "N",
    sectionsLabel: "Bereiche",
    sections: ["Top", "Launches", "Design", "KI", "Märkte", "Tools"],
    kicker: "Live-Bericht",
    latest: "Neueste Meldungen",
    more: "Mehr",
    done: "Alles aktuell",
    toast: "Weitere Meldungen geladen",
    points: "Punkte",
    comments: "Kommentare",
    pages: []
  },
  "fr-FR": {
    lang: "fr-FR",
    dir: "ltr",
    title: "Northstar News",
    mark: "N",
    sectionsLabel: "Rubriques",
    sections: ["À la une", "Lancements", "Design", "IA", "Marchés", "Outils"],
    kicker: "Couverture en direct",
    latest: "Dernières actus",
    more: "Plus",
    done: "Tout est à jour",
    toast: "Plus d'actus chargées",
    points: "points",
    comments: "commentaires",
    pages: []
  },
  "es-ES": {
    lang: "es-ES",
    dir: "ltr",
    title: "Northstar News",
    mark: "N",
    sectionsLabel: "Secciones",
    sections: ["Principal", "Lanzamientos", "Diseño", "IA", "Mercados", "Herramientas"],
    kicker: "Cobertura en directo",
    latest: "Últimas noticias",
    more: "Más",
    done: "Todo al día",
    toast: "Más noticias cargadas",
    points: "puntos",
    comments: "comentarios",
    pages: []
  },
  "pt-PT": {
    lang: "pt-PT",
    dir: "ltr",
    title: "Northstar News",
    mark: "N",
    sectionsLabel: "Secções",
    sections: ["Topo", "Lançamentos", "Design", "IA", "Mercados", "Ferramentas"],
    kicker: "Cobertura em direto",
    latest: "Últimas notícias",
    more: "Mais",
    done: "Tudo atualizado",
    toast: "Mais notícias carregadas",
    points: "pontos",
    comments: "comentários",
    pages: []
  },
  "ar-SA": {
    lang: "ar-SA",
    dir: "rtl",
    title: "أخبار نورث ستار",
    mark: "ن",
    sectionsLabel: "الأقسام",
    sections: ["الأهم", "الإطلاقات", "التصميم", "الذكاء الاصطناعي", "الأسواق", "الأدوات"],
    kicker: "تغطية مباشرة",
    latest: "آخر الأخبار",
    more: "المزيد",
    done: "تم التحديث",
    toast: "تم تحميل المزيد من الأخبار",
    points: "نقطة",
    comments: "تعليق",
    pages: []
  }
};

const BASE_TRANSLATABLE_PAGES = {
  "zh-Hant": [
    {
      count: "第 1 / 30 頁",
      live: "剛剛更新",
      headline: "獨立開發者正在更快地發布行動產品。",
      summary: "過去一小時的產品發布、工具更新與產業動態摘要。",
      stories: [
        ["一款輕量編輯器簡化發布筆記", "18 分", "4 則留言"],
        ["小團隊如何處理午夜版本發布", "31 分", "12 則留言"],
        ["新的儀表板即時追蹤候補名單", "27 分", "8 則留言"],
        ["讓小型 App 更快的設計細節", "22 分", "6 則留言"],
        ["開發者測試更精簡的結帳流程", "19 分", "3 則留言"],
        ["一次產品展示日的現場記錄", "15 分", "2 則留言"]
      ]
    },
    {
      count: "第 2 / 30 頁",
      live: "5 秒前更新",
      headline: "新的產品發布正從等待名單走向公開。",
      summary: "即時資訊流的下一頁已經出現新的內容。",
      stories: [
        ["晶片新創公司發布首款開發套件", "86 分", "24 則留言"],
        ["行事曆 App 加入共享預約頁面", "74 分", "19 則留言"],
        ["一家新創公布新的定價實驗", "61 分", "14 則留言"],
        ["開源資料庫專案加入向量搜尋", "58 分", "11 則留言"],
        ["設計師分享更清爽的行動設定面板", "43 分", "9 則留言"],
        ["小型 App 憑藉清晰引導贏得用戶", "39 分", "7 則留言"]
      ]
    },
    {
      count: "第 3 / 30 頁",
      live: "10 秒前更新",
      headline: "最後一批內容加入後續分析與讀者筆記。",
      summary: "本次工作階段已到達最新一組資訊。",
      stories: [
        ["今日發布報導的讀者筆記", "97 分", "31 則留言"],
        ["最新產品發布之後發生了什麼", "88 分", "22 則留言"],
        ["團隊交流現場展示日經驗", "76 分", "17 則留言"],
        ["公開狀態頁的實用指南", "64 分", "13 則留言"],
        ["開發者文件加入新的 API 範例", "52 分", "10 則留言"],
        ["午前完成發布的週末專案", "49 分", "8 則留言"]
      ]
    }
  ]
};

function translatedPages(locale, commentsWord) {
  if (BASE_TRANSLATABLE_PAGES[locale]) return BASE_TRANSLATABLE_PAGES[locale];
  const source = I18N[FALLBACK].pages;
  const config = {
    "ja": {
      counts: ["30ページ中1ページ", "30ページ中2ページ", "30ページ中3ページ"],
      lives: ["たった今更新", "5秒前に更新", "10秒前に更新"],
      headlines: [
        "小さなチームがモバイルでより速く出荷しています。",
        "新しいローンチが公開リリースへ進んでいます。",
        "最後の更新に読者メモと分析が加わりました。"
      ],
      summaries: [
        "過去1時間のローンチ、製品ニュース、業界アップデートのまとめです。",
        "ライブフィードの次のページから新しい更新が届きました。",
        "このセッションの最新ストーリーに到達しました。"
      ],
      storyPrefix: ["モバイル向け新機能", "チームのリリースメモ", "リアルタイム待機リスト", "高速化した設計", "チェックアウト実験", "デモ日の現場レポート"]
    },
    "ko": {
      counts: ["30쪽 중 1쪽", "30쪽 중 2쪽", "30쪽 중 3쪽"],
      lives: ["방금 업데이트됨", "5초 전 업데이트됨", "10초 전 업데이트됨"],
      headlines: [
        "작은 팀들이 모바일에서 더 빠르게 출시하고 있습니다.",
        "새로운 출시 소식이 공개 단계로 이동하고 있습니다.",
        "마지막 묶음에 후속 분석과 독자 메모가 추가되었습니다."
      ],
      summaries: [
        "지난 한 시간의 출시, 제품 소식, 업계 업데이트를 모았습니다.",
        "라이브 피드의 다음 페이지에서 새 업데이트를 찾았습니다.",
        "이번 세션의 최신 소식 묶음에 도달했습니다."
      ],
      storyPrefix: ["빠른 출시 노트 편집기", "작은 팀의 릴리스 운영", "실시간 대기자 명단", "더 빠른 모바일 디자인", "체크아웃 실험", "제품 데모 현장 기록"]
    },
    "de-DE": {
      counts: ["Seite 1 von 30", "Seite 2 von 30", "Seite 3 von 30"],
      lives: ["Gerade aktualisiert", "Vor 5 Sek. aktualisiert", "Vor 10 Sek. aktualisiert"],
      headlines: [
        "Unabhängige Entwickler liefern mobil schneller aus.",
        "Neue Launches wechseln von Wartelisten zur Veröffentlichung.",
        "Der letzte Block ergänzt Analyse und Lesernotizen."
      ],
      summaries: [
        "Ein laufender Überblick über Launches, Produktnews und Branchenupdates der letzten Stunde.",
        "Auf der nächsten Seite des Live-Feeds sind neue Updates verfügbar.",
        "Der Feed hat die neuesten Meldungen dieser Sitzung erreicht."
      ],
      storyPrefix: ["Kompakter Editor für Launch-Notizen", "Kleines Team steuert Nacht-Release", "Dashboard verfolgt Wartelisten", "Design macht Apps schneller", "Entwickler testen Checkout", "Bericht vom Produkt-Demo-Tag"]
    },
    "fr-FR": {
      counts: ["Page 1 sur 30", "Page 2 sur 30", "Page 3 sur 30"],
      lives: ["Mis à jour à l'instant", "Mis à jour il y a 5 s", "Mis à jour il y a 10 s"],
      headlines: [
        "Les équipes indépendantes livrent plus vite sur mobile.",
        "De nouveaux lancements passent de la liste d'attente au public.",
        "Le dernier lot ajoute analyses et notes de lecteurs."
      ],
      summaries: [
        "Un condensé des lancements, nouveautés produit et actualités du secteur de la dernière heure.",
        "De nouvelles mises à jour sont disponibles sur la page suivante du flux.",
        "Le flux a atteint les dernières actus de cette session."
      ],
      storyPrefix: ["Éditeur compact pour notes de lancement", "Une petite équipe gère une sortie nocturne", "Tableau de bord des listes d'attente", "Détails de design plus rapides", "Expérience de paiement", "Retour d'une journée de démo"]
    },
    "es-ES": {
      counts: ["Página 1 de 30", "Página 2 de 30", "Página 3 de 30"],
      lives: ["Actualizado ahora", "Actualizado hace 5 s", "Actualizado hace 10 s"],
      headlines: [
        "Los equipos independientes lanzan más rápido en móvil.",
        "Nuevos lanzamientos pasan de la lista de espera al público.",
        "El último bloque añade análisis y notas de lectores."
      ],
      summaries: [
        "Resumen continuo de lanzamientos, noticias de producto y novedades del sector de la última hora.",
        "Ya hay actualizaciones nuevas en la siguiente página del feed.",
        "El feed llegó al último grupo de noticias de esta sesión."
      ],
      storyPrefix: ["Editor compacto para notas de lanzamiento", "Un equipo pequeño gestiona un lanzamiento nocturno", "Panel de listas de espera", "Diseño que acelera una app", "Prueba de checkout", "Informe de un día de demo"]
    },
    "pt-PT": {
      counts: ["Página 1 de 30", "Página 2 de 30", "Página 3 de 30"],
      lives: ["Atualizado agora", "Atualizado há 5 s", "Atualizado há 10 s"],
      headlines: [
        "Equipas independentes estão a lançar mais depressa no mobile.",
        "Novos lançamentos passam da lista de espera para o público.",
        "O último bloco junta análise e notas de leitores."
      ],
      summaries: [
        "Um resumo contínuo de lançamentos, notícias de produto e atualizações da última hora.",
        "Há novas atualizações na página seguinte do feed ao vivo.",
        "O feed chegou ao conjunto mais recente desta sessão."
      ],
      storyPrefix: ["Editor compacto para notas de lançamento", "Equipa pequena gere uma versão noturna", "Painel acompanha listas de espera", "Detalhes de design mais rápidos", "Experiência de checkout", "Relato de um dia de demonstração"]
    },
    "ar-SA": {
      counts: ["الصفحة 1 من 30", "الصفحة 2 من 30", "الصفحة 3 من 30"],
      lives: ["تم التحديث الآن", "تم التحديث قبل 5 ثوان", "تم التحديث قبل 10 ثوان"],
      headlines: [
        "الفرق المستقلة تطلق منتجات الجوال بسرعة أكبر.",
        "إطلاقات جديدة تنتقل من قوائم الانتظار إلى الجمهور.",
        "الدفعة الأخيرة تضيف تحليلاً وملاحظات القراء."
      ],
      summaries: [
        "ملخص متجدد لإطلاقات المنتجات وأخبار الأدوات وتحديثات القطاع خلال الساعة الماضية.",
        "تتوفر تحديثات جديدة الآن في الصفحة التالية من الموجز المباشر.",
        "وصل الموجز إلى أحدث مجموعة أخبار في هذه الجلسة."
      ],
      storyPrefix: ["محرر ملاحظات إطلاق سريع", "فريق صغير يدير إصداراً ليلياً", "لوحة تتابع قوائم الانتظار", "تفاصيل تصميم تجعل التطبيق أسرع", "تجربة دفع جديدة", "تقرير من يوم عرض المنتج"]
    }
  }[locale];

  if (!config) return source;
  return source.map((page, pageIndex) => ({
    count: config.counts[pageIndex],
    live: config.lives[pageIndex],
    headline: config.headlines[pageIndex],
    summary: config.summaries[pageIndex],
    stories: page.stories.map((story, storyIndex) => [
      config.storyPrefix[storyIndex],
      story[1].replace("points", I18N[locale].points || "points"),
      story[2].replace("comments", commentsWord)
    ])
  }));
}

function detectLocale() {
  const explicit = document.documentElement.dataset.locale;
  if (explicit && I18N[explicit]) return explicit;
  const file = window.location.pathname.split("/").pop().replace(/\.html$/i, "");
  const match = file.match(/^video-(.+)$/i);
  if (!match) return FALLBACK;
  return LOCALE_ALIASES[match[1].toLowerCase()] || FALLBACK;
}

const locale = detectLocale();
const data = I18N[locale] || I18N[FALLBACK];
if (!data.pages.length) data.pages = translatedPages(locale, data.comments);

const EXTRA_PAGE_COPY = {
  "en-US": {
    counts: ["Page 4 of 30", "Page 5 of 30", "Page 6 of 30", "Page 7 of 30", "Page 8 of 30"],
    lives: ["Updated 15 sec ago", "Updated 20 sec ago", "Updated 25 sec ago", "Updated 30 sec ago", "Updated 35 sec ago"],
    headlines: [
      "Another update brings more field notes from small teams.",
      "Fresh activity appears as the page keeps moving.",
      "The live feed keeps adding useful follow-up stories.",
      "More reports arrive as the queue keeps moving.",
      "A final preview page shows the loop continuing."
    ],
    summaries: [
      "New reports continue to arrive while Safari keeps the feed moving.",
      "The next page shows more launches, product notes, and user updates.",
      "Repeated refresh and click actions can keep browsing through matching pages.",
      "Each automatic click advances to the next matching result in the feed.",
      "The demo keeps enough pages available for a clean preview recording."
    ],
    stories: [
      "A small product team shares its launch checklist",
      "A booking tool adds faster confirmation screens",
      "Creators compare notes from a live feedback session",
      "A dashboard highlights changes in active queues",
      "Design teams simplify a crowded mobile workflow",
      "A new report tracks early customer reactions"
    ]
  },
  "zh-Hans": {
    counts: ["第 4 / 30 页", "第 5 / 30 页", "第 6 / 30 页", "第 7 / 30 页", "第 8 / 30 页"],
    lives: ["15 秒前更新", "20 秒前更新", "25 秒前更新", "30 秒前更新", "35 秒前更新"],
    headlines: [
      "新的动态继续带来小团队的一线记录。",
      "页面持续前进时，又出现了新的内容。",
      "实时信息流继续加入有用的后续报道。",
      "队列持续变化时，更多报道继续出现。",
      "最后一页预览展示循环仍在继续。"
    ],
    summaries: [
      "Safari 持续刷新和点击时，新的报道会继续进入信息流。",
      "下一页展示更多发布、产品记录和用户反馈。",
      "重复刷新和点击可以帮助用户继续浏览匹配页面。",
      "每次自动点击都会前进到信息流里的下一个匹配结果。",
      "Demo 保留足够的页面，让预览视频录制更干净。"
    ],
    stories: [
      "小型产品团队分享发布检查清单",
      "预约工具加入更快的确认页面",
      "创作者交流现场反馈经验",
      "看板突出显示活跃队列变化",
      "设计团队简化拥挤的移动流程",
      "新的报告追踪早期用户反馈"
    ]
  },
  "zh-Hant": {
    counts: ["第 4 / 30 頁", "第 5 / 30 頁", "第 6 / 30 頁", "第 7 / 30 頁", "第 8 / 30 頁"],
    lives: ["15 秒前更新", "20 秒前更新", "25 秒前更新", "30 秒前更新", "35 秒前更新"],
    headlines: [
      "新的動態繼續帶來小團隊的一線記錄。",
      "頁面持續前進時，又出現了新的內容。",
      "即時資訊流繼續加入有用的後續報導。",
      "佇列持續變化時，更多報導繼續出現。",
      "最後一頁預覽展示循環仍在繼續。"
    ],
    summaries: [
      "Safari 持續刷新和點擊時，新的報導會繼續進入資訊流。",
      "下一頁展示更多發布、產品記錄和用戶回饋。",
      "重複刷新和點擊可以幫助用戶繼續瀏覽匹配頁面。",
      "每次自動點擊都會前進到資訊流裡的下一個匹配結果。",
      "Demo 保留足夠的頁面，讓預覽影片錄製更乾淨。"
    ],
    stories: [
      "小型產品團隊分享發布檢查清單",
      "預約工具加入更快的確認頁面",
      "創作者交流現場回饋經驗",
      "儀表板突出顯示活躍佇列變化",
      "設計團隊簡化擁擠的行動流程",
      "新的報告追蹤早期用戶回饋"
    ]
  }
};

function extraPageCopy(locale) {
  if (EXTRA_PAGE_COPY[locale]) return EXTRA_PAGE_COPY[locale];
  const base = EXTRA_PAGE_COPY[FALLBACK];
  const labels = {
    "ja": {
      counts: ["30ページ中4ページ", "30ページ中5ページ", "30ページ中6ページ", "30ページ中7ページ", "30ページ中8ページ"],
      lives: ["15秒前に更新", "20秒前に更新", "25秒前に更新", "30秒前に更新", "35秒前に更新"]
    },
    "ko": {
      counts: ["30쪽 중 4쪽", "30쪽 중 5쪽", "30쪽 중 6쪽", "30쪽 중 7쪽", "30쪽 중 8쪽"],
      lives: ["15초 전 업데이트됨", "20초 전 업데이트됨", "25초 전 업데이트됨", "30초 전 업데이트됨", "35초 전 업데이트됨"]
    },
    "de-DE": {
      counts: ["Seite 4 von 30", "Seite 5 von 30", "Seite 6 von 30", "Seite 7 von 30", "Seite 8 von 30"],
      lives: ["Vor 15 Sek. aktualisiert", "Vor 20 Sek. aktualisiert", "Vor 25 Sek. aktualisiert", "Vor 30 Sek. aktualisiert", "Vor 35 Sek. aktualisiert"]
    },
    "fr-FR": {
      counts: ["Page 4 sur 30", "Page 5 sur 30", "Page 6 sur 30", "Page 7 sur 30", "Page 8 sur 30"],
      lives: ["Mis à jour il y a 15 s", "Mis à jour il y a 20 s", "Mis à jour il y a 25 s", "Mis à jour il y a 30 s", "Mis à jour il y a 35 s"]
    },
    "es-ES": {
      counts: ["Página 4 de 30", "Página 5 de 30", "Página 6 de 30", "Página 7 de 30", "Página 8 de 30"],
      lives: ["Actualizado hace 15 s", "Actualizado hace 20 s", "Actualizado hace 25 s", "Actualizado hace 30 s", "Actualizado hace 35 s"]
    },
    "pt-PT": {
      counts: ["Página 4 de 30", "Página 5 de 30", "Página 6 de 30", "Página 7 de 30", "Página 8 de 30"],
      lives: ["Atualizado há 15 s", "Atualizado há 20 s", "Atualizado há 25 s", "Atualizado há 30 s", "Atualizado há 35 s"]
    },
    "ar-SA": {
      counts: ["الصفحة 4 من 30", "الصفحة 5 من 30", "الصفحة 6 من 30", "الصفحة 7 من 30", "الصفحة 8 من 30"],
      lives: ["تم التحديث قبل 15 ثانية", "تم التحديث قبل 20 ثانية", "تم التحديث قبل 25 ثانية", "تم التحديث قبل 30 ثانية", "تم التحديث قبل 35 ثانية"]
    }
  }[locale] || {};
  return { ...base, ...labels };
}

function ensureEightPages(locale) {
  if (data.pages.length >= 8) return;
  const copy = extraPageCopy(locale);
  const points = ["82", "69", "57", "44", "36", "28"];
  const comments = ["23", "16", "11", "8", "5", "3"];
  while (data.pages.length < 8) {
    const extraIndex = data.pages.length - 3;
    data.pages.push({
      count: copy.counts[extraIndex],
      live: copy.lives[extraIndex],
      headline: copy.headlines[extraIndex],
      summary: copy.summaries[extraIndex],
      stories: copy.stories.map((title, storyIndex) => [
        title,
        `${points[storyIndex]} ${locale === "en-US" ? "points" : locale.startsWith("zh") ? "分" : I18N[locale].points || "points"}`,
        `${comments[storyIndex]} ${data.comments}`
      ])
    });
  }
}

ensureEightPages(locale);

function initialPageIndex() {
  try {
    const url = new URL(window.location.href);
    const value = Number.parseInt(url.searchParams.get("autoRefreshPreviewPage") || "1", 10);
    if (Number.isFinite(value)) {
      return Math.min(Math.max(value - 1, 0), data.pages.length - 1);
    }
  } catch (error) {
    return 0;
  }
  return 0;
}

function updatePreviewPageUrl() {
  try {
    const url = new URL(window.location.href);
    if (pageIndex > 0) {
      url.searchParams.set("autoRefreshPreviewPage", String(pageIndex + 1));
    } else {
      url.searchParams.delete("autoRefreshPreviewPage");
    }
    window.history.replaceState({}, "", url);
  } catch (error) {
    // Keep the demo usable even when history updates are unavailable.
  }
}

let pageIndex = initialPageIndex();
let keepTargetAvailable = false;
try {
  keepTargetAvailable = new URL(window.location.href).searchParams.get("autoRefreshPreviewKeepTarget") === "1";
} catch (error) {
  keepTargetAvailable = false;
}
const storyList = document.getElementById("storyList");
const moreButton = document.getElementById("moreButton");
const pageCount = document.getElementById("pageCount");
const liveText = document.getElementById("liveText");
const headline = document.getElementById("headline");
const summary = document.getElementById("summary");
const toast = document.getElementById("toast");

document.documentElement.lang = data.lang;
document.documentElement.dir = data.dir;
document.title = data.title;
document.getElementById("brandMark").textContent = data.mark;
document.getElementById("brandName").textContent = data.title;
document.getElementById("sectionsNav").setAttribute("aria-label", data.sectionsLabel);
document.getElementById("kicker").textContent = data.kicker;
document.getElementById("latestLabel").textContent = data.latest;
toast.textContent = data.toast;
document.getElementById("sectionsNav").innerHTML = data.sections.map(section => `<span>${section}</span>`).join("");
document.querySelector(".feed").setAttribute("aria-label", data.latest);

function renderPage(isNew) {
  const page = data.pages[pageIndex];
  pageCount.textContent = page.count;
  liveText.textContent = page.live;
  headline.textContent = page.headline;
  summary.textContent = page.summary;
  storyList.innerHTML = page.stories.map((story, index) => `
    <article class="story${isNew ? " is-new" : ""}" style="animation-delay:${index * 42}ms">
      <div class="rank">${pageIndex * 6 + index + 1}</div>
      <div>
        <div class="title">${story[0]}</div>
        <div class="meta"><span class="hot">${story[1]}</span><span>${story[2]}</span></div>
      </div>
    </article>
  `).join("");
  const isLastPage = pageIndex >= data.pages.length - 1;
  moreButton.textContent = isLastPage && !keepTargetAvailable ? data.done : data.more;
  moreButton.disabled = isLastPage && !keepTargetAvailable;
}

function showToast() {
  toast.classList.add("show");
  window.setTimeout(() => toast.classList.remove("show"), 1700);
}

moreButton.addEventListener("click", () => {
  if (pageIndex >= data.pages.length - 1) return;
  pageIndex += 1;
  updatePreviewPageUrl();
  renderPage(true);
});

renderPage(false);
