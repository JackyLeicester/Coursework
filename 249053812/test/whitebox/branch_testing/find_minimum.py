class MINIMUMVALUE:
    @staticmethod
    def find_min(nums):
        if len(nums) == 0:
            return 0
        elif len(nums) == 1:
            return nums[0]
        low, high = 0, len(nums) - 1
        while low < high:
            mid = (low + high) // 2
            if mid > 0 and nums[mid] < nums[mid - 1]:
                return nums[mid]
            if nums[low] > nums[mid]:
                high = mid - 1
            elif nums[high] < nums[mid]:
                low = mid + 1
            else:
                high = mid - 1
        return nums[low]
