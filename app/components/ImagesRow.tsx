import prisma from "../lib/db";
import { Skeleton } from "@/components/ui/skeleton";
import { ImageCard, LoadingProductCard } from "./ImageCard";
import { Suspense } from "react";

async function getData() {
  const data = await prisma.nASA.findMany({
    select: {
      id: true,
      image_url: true,
      Constellation: true,
    },
  });

  return {
    data: data,
  };
}

export async function ImagesRow() {
  const data = await getData();
  return (
    <section className="mt-12">
      <Suspense fallback={<LoadingState />}>
        <LoadRows />
      </Suspense>
    </section>
  );
}

async function LoadRows() {
  const data = await getData();
  return (
    <>
      <div className="grid grid-cols-1 lg:grid-cols-3 sm:grid-cols-2 mt-4 gap-10">
        {data.data.map((image) => (
          <ImageCard
            id={image.id}
            key={image.id}
            imageUrl={image.image_url}
            title={image.Constellation}
          />
        ))}
      </div>
    </>
  );
}

function LoadingState() {
  return (
    <div>
      <Skeleton className="h-8 w-56" />
      <div className="grid grid-cols-1 sm:grid-cols-2 mt-4 gap-10 lg:grid-cols-3">
        <LoadingProductCard />
        <LoadingProductCard />
        <LoadingProductCard />
      </div>
    </div>
  );
}
