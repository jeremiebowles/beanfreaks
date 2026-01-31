import { defineCollection, z } from "astro:content";

const stores = defineCollection({
  type: "content",
  schema: z.object({
    name: z.string(),
    address: z.string(),
    phone: z.string(),
    map_url: z.string().url(),
    hours_summary: z.string(),
    hours: z.array(z.object({
      day: z.string(),
      open: z.string(),
      close: z.string()
    })).default([]),
    highlights: z.array(z.string()).default([])
  })
});

const offers = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    expires: z.coerce.date().optional(),
    featured: z.boolean().default(false),
    summary: z.string()
  })
});

const guides = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    summary: z.string(),
    tags: z.array(z.string()).default([])
  })
});

export const collections = { stores, offers, guides };
