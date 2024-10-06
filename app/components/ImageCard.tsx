import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import Link from "next/link";

interface iAppProps {
  id: string;
  imageUrl: string;
  title: string;
}

export function ImageCard({ id, imageUrl, title }: iAppProps) {
  return (
    <>
      <div className="rounded-lg">
        <div className="relative h-[350px]">
          <Image
            alt="Article Image"
            src={imageUrl}
            layout="fill"
            objectFit="cover"
            className="object-cover h-full w-full rounded-lg"
          />
        </div>

        <div className="flex justify-between items-center mt-2">
          <h1 className="font-semibold text-xl line-clamp-3">{title}</h1>
        </div>

        <Button asChild className="w-full mt-5">
          <Link href={`/article/${id}`}>Explore</Link>
        </Button>
      </div>
    </>
  );
}

export function LoadingProductCard() {
  return (
    <div className="flex flex-col">
      <Skeleton className="w-full h-[230px]" />
      <div className="flex flex-col mt-2 gap-y-2">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="w-full h-6" />
      </div>

      <Skeleton className="w-full h-10 mt-5" />
    </div>
  );
}
