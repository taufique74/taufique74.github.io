import type { CollectionEntry } from "astro:content";
import { SITE } from "@/config";

const postFilter = ({ data }: CollectionEntry<"blog">) => {
  const isPublishTimePassed =
    Date.now() >
    new Date(data.pubDatetime).getTime() - SITE.scheduledPostMargin;
  // Locally, show everything so drafts and scheduled posts can be previewed.
  // A production build still excludes both.
  return import.meta.env.DEV || (!data.draft && isPublishTimePassed);
};

export default postFilter;
