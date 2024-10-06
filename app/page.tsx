import { ImagesRow } from "./components/ImagesRow";

export default function Home() {
  return (
    <section className="max-w-7xl mx-auto px-4 md:px-8 mb-24">
      <div className="max-w-3xl mx-auto text-2xl sm:text-5xl lg:text-6xl font-semibold text-center">
        {/* <h1>NASA Project</h1>
        <p className="lg:text-lg text-muted-foreground mx-auto mt-5 w-[90%] font-normal text-base">
          Turning images into stories
        </p> */}
        <ImagesRow />
      </div>
    </section>
  );
}
