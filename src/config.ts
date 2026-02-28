export const SITE = {
  website: "https://tpeyash.com/",
  author: "Taufique Peyash",
  profile: "https://github.com/taufique74",
  desc: "Notes from the bench — on speech AI, machine learning, and the craft of building systems that learn.",
  title: "Peyash's Logs",
  ogImage: "astropaper-og.jpg",
  lightAndDarkMode: true,
  postPerIndex: 4,
  postPerPage: 4,
  scheduledPostMargin: 15 * 60 * 1000, // 15 minutes
  showArchives: true,
  showBackButton: true,
  editPost: {
    enabled: false,
    text: "Edit page",
    url: "https://github.com/taufique74/taufique74.github.io/edit/main/",
  },
  dynamicOgImage: true,
  dir: "ltr",
  lang: "en",
  timezone: "America/New_York",
} as const;
