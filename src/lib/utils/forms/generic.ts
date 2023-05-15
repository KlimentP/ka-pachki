export const handleModalFormErrors = (error: any) => {
    if (error) {
        return {error: error.message};
    }
    return {message: 'Success'};
}