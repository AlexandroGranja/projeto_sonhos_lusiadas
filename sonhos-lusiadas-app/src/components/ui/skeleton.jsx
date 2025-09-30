import { cn } from "@/lib/utils"

const Skeleton = ({ className, ...props }) => {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-slate-200", className)}
      {...props}
    />
  )
}

const SkeletonCard = ({ className, ...props }) => {
  return (
    <div
      className={cn(
        "rounded-lg border border-slate-200 p-6 space-y-4",
        className
      )}
      {...props}
    >
      <div className="space-y-2">
        <Skeleton className="h-4 w-3/4" />
        <Skeleton className="h-4 w-1/2" />
      </div>
      <Skeleton className="h-8 w-16" />
    </div>
  )
}

const SkeletonTable = ({ rows = 5, className, ...props }) => {
  return (
    <div className={cn("space-y-4", className)} {...props}>
      {[...Array(rows)].map((_, i) => (
        <div key={i} className="flex items-center space-x-4">
          <Skeleton className="h-10 w-10 rounded-full" />
          <div className="space-y-2 flex-1">
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-3 w-1/2" />
          </div>
          <Skeleton className="h-6 w-16" />
        </div>
      ))}
    </div>
  )
}

export { Skeleton, SkeletonCard, SkeletonTable }