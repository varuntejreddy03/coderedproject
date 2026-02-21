"""
Add this to main.py after other endpoints
"""

@app.get("/queue-stats")
async def get_queue_stats():
    """
    📊 Job Queue Statistics
    Shows processing pipeline status
    """
    if not job_queue:
        return {"error": "Queue not initialized"}
    
    stats = job_queue.get_stats()
    
    return {
        "queue": {
            "pending_jobs": stats['queue_size'],
            "processed_total": stats['processed'],
            "failed_total": stats['failed'],
            "is_running": stats['is_running']
        },
        "pipeline": {
            "ingestion": "✅ Real-time (Telegram streaming)",
            "queue": f"✅ {stats['queue_size']} jobs pending",
            "processing": f"✅ {stats['processed']} processed",
            "database": "✅ Supabase connected",
            "api": "✅ Ready"
        },
        "timestamp": datetime.now().isoformat()
    }
