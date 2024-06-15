"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm} from "react-hook-form"
import { z } from "zod"

import { Button } from "@/components/ui/button"
import {Form,FormControl,FormDescription,FormField,FormItem,FormLabel,FormMessage} from "@/components/ui/form"
import {Select,SelectContent,SelectItem,SelectTrigger,SelectValue,} from "@/components/ui/select"
import { toast } from "@/components/ui/use-toast"
import { Input } from "@/components/ui/input"

import axios from 'axios';

const formSchema = z.object({
    search_term: z.string().min(2, {
      message: "Search term must be at least 2 characters.",
    }),
    depth: z.number({
      required_error: "Please select a depth.",
    })
})

export function StartScrape() {
    const defaultValues = {
        search_term: "",
        depth: 2
    }

    const form = useForm<z.infer<typeof formSchema>>({// 1. Define your form.
      resolver: zodResolver(formSchema),
      defaultValues,
    })
    
    async function onSubmit(values: z.infer<typeof formSchema>) {// 2. Define a submit handler.
        toast({
            title: "You submitted the following values:",
            description: (
                <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
                <code className="text-white">{JSON.stringify(values, null, 2)}</code>
                </pre>
            ),
        })
        form.reset(defaultValues)
  
        try {
            const response = await axios.post('/api/start-scraping', values); 
            toast({
              title: "Success!",
              description: (
                  <p className="leading-7 [&:not(:first-child)]:mt-6">{response.data.message}</p>
              ),
            })
          } catch (error) {
            toast({
              title: "Something went wrong!",
            })
          }
        }

    return (
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
          <h3 className="scroll-m-20 text-2xl font-semibold tracking-tight">Start Scraping Process</h3>
            <FormField
              control={form.control}
              name="search_term"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Search Term</FormLabel>
                  <FormControl>
                    <Input placeholder="Hunter Biden" {...field} />
                  </FormControl>
                  <FormDescription>
                    Please provide a relevant search term.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
                control={form.control}
                name="depth"
                render={({ field }) => (
                    <FormItem>
                    <FormLabel>Max Scraping Depth</FormLabel>
                    <Select 
                        onValueChange={(value : string) => field.onChange(Number(value))} 
                        defaultValue={field.value !== undefined ? field.value.toString() : "2"}
                        value={field.value?.toString() || "2"}
                    >
                        <FormControl>
                        <SelectTrigger>
                            <SelectValue placeholder="Please select a max depth to scrape." />
                        </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                            <SelectItem value="2">{2}</SelectItem>
                            <SelectItem value="3">{3}</SelectItem>
                            <SelectItem value="4">{4}</SelectItem>
                            <SelectItem value="5">{5}</SelectItem>
                            <SelectItem value="6">{6}</SelectItem>
                        </SelectContent>
                    </Select>
                    <FormDescription>
                        Be aware that the more depth you go the longer it will take to scrape.
                    </FormDescription>
                    <FormMessage />
                    </FormItem>
                )}
                />
            <Button type="submit">Submit</Button>
          </form>
        </Form>
      )
  }